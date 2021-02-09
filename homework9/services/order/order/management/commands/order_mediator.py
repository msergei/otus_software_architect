import sys
import json
import time
import signal
import requests

import redis
from retry import retry
from django.core.management.base import BaseCommand
from django.conf import settings
from rest_framework import status

from order.models import Order


class OrderMediator(object):

    def start_order(self, order):
        ordering = (self.make_payment, self.reserve_item, self.post_delivery)

        for i, exec_stage in enumerate(ordering):
            if not exec_stage(order):
                self.cancel_order(order, i)
                return False

        print(f'Order {order} was completed')
        Order.objects.filter(id=order['id']).update(success=True)
        return True

    def make_payment(self, order):
        response = requests.get(f'{settings.BILLING_URL}/{order["username"]}')

        if response.status_code != status.HTTP_200_OK:
            return False

        account = response.json()
        wallet = account['wallet']

        if wallet < order['amount']:
            print(f'Not enough money to create order {order}')
            return False

        wallet -= order['amount']
        response = requests.patch(f'{settings.BILLING_URL}/{order["username"]}', data={'wallet': wallet})

        if response.status_code != status.HTTP_200_OK:
            print(f'Order {order} did not create, details: {response.text}')
            return False

        return True

    def reserve_item(self, order):
        url = f'{settings.ITEM_URL}/reserve/{order["details"]["item"]}'

        response = requests.patch(url, data={'username': order['username']})
        if response.status_code != status.HTTP_200_OK:
            print(f'Could not reserve the item, order: {order}')
            return False

        return True

    def post_delivery(self, order):
        url = f'{settings.DELIVERY_URL}/{order["details"]["slot"]}'

        response = requests.patch(url, data={'username': order['username']})
        if response.status_code != status.HTTP_200_OK:
            print(f'Could not reserve the slot, order: {order}')
            return False

        return True

    @retry()
    def cancel_order(self, order, stage=2):
        CANCELATION_REASON = {
            0: 'Not enough money',
            1: 'Can not reserve the item',
            2: 'Can not get the delivery slot',
        }

        canceling = (self.cancel_payment, self.cancel_reserve,)

        for cancel_func in canceling[:stage]:
            cancel_func(order)

        Order.objects.filter(id=order['id']).update(success=False, reason=CANCELATION_REASON[stage])
        print(f'Order {order} was canceled')
        return True

    @retry()
    def cancel_payment(self, order):
        response = requests.get(f'{settings.BILLING_URL}/{order["username"]}')

        if response.status_code != status.HTTP_200_OK:
            return False

        account = response.json()
        wallet = account['wallet']

        wallet += order['amount']
        response = requests.patch(f'{settings.BILLING_URL}/{order["username"]}', data={'wallet': wallet})

        if response.status_code != status.HTTP_200_OK:
            return False

        return True

    @retry()
    def cancel_reserve(self, order):
        url = f'{settings.ITEM_URL}/cancel/{order["details"]["item"]}'

        response = requests.patch(url, data={'username': None})
        if response.status_code != status.HTTP_200_OK:
            return False

        return True


class Command(BaseCommand):
    help = 'Order SAGA mediator'

    def receive_signal(self, signal_number, frame):
        print(f'Received {signal_number}, lets shutdown')
        self.stdout.write(self.style.SUCCESS('Lets shutdown'))
        sys.exit()

    def signal_register(self):
        signal.signal(signal.SIGHUP, self.receive_signal)
        signal.signal(signal.SIGINT, self.receive_signal)
        signal.signal(signal.SIGQUIT, self.receive_signal)
        signal.signal(signal.SIGILL, self.receive_signal)
        signal.signal(signal.SIGTRAP, self.receive_signal)
        signal.signal(signal.SIGABRT, self.receive_signal)
        signal.signal(signal.SIGBUS, self.receive_signal)
        signal.signal(signal.SIGFPE, self.receive_signal)
        # signal.signal(signal.SIGKILL, self.receive_signal)
        signal.signal(signal.SIGUSR1, self.receive_signal)
        signal.signal(signal.SIGSEGV, self.receive_signal)
        signal.signal(signal.SIGUSR2, self.receive_signal)
        signal.signal(signal.SIGPIPE, self.receive_signal)
        signal.signal(signal.SIGALRM, self.receive_signal)
        signal.signal(signal.SIGTERM, self.receive_signal)

    def handle(self, *args, **options):
        self.signal_register()
        mediator = OrderMediator()

        conn = redis.Redis(host=settings.REDIS_HOST, port=6379, db=0)

        print('Lets start listen events')

        while True:
            data = conn.lpop(settings.ORDER_QUEUE)
            if data:
                order = json.loads(data)
                mediator.start_order(order)

            time.sleep(1)
