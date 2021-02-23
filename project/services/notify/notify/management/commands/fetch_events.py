import json
import signal
import sys
import time

import redis
from django.conf import settings
from django.core.management.base import BaseCommand

from notify.models import History, Notification


class RedisBridge(object):
    HISTORY = 'history'
    NOTIFY = 'notify'

    def __init__(self):
        self.conn = redis.Redis(host=settings.REDIS_HOST, port=6379, db=0)

    def get_order(self, queue):
        data = self.conn.lpop(queue)
        if data:
            order = json.loads(data)
            return order


class Command(BaseCommand):
    help = 'History and notification fetcher'

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
        signal.signal(signal.SIGUSR1, self.receive_signal)
        signal.signal(signal.SIGSEGV, self.receive_signal)
        signal.signal(signal.SIGUSR2, self.receive_signal)
        signal.signal(signal.SIGPIPE, self.receive_signal)
        signal.signal(signal.SIGALRM, self.receive_signal)
        signal.signal(signal.SIGTERM, self.receive_signal)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_client = RedisBridge()

    def get_notification(self):
        order = self.redis_client.get_order(RedisBridge.NOTIFY)
        if not order:
            return
        Notification.objects.create(
            username=order['user'],
            success=order['success'],
            message=f'Order with id {order["id"]} was complete'
        )
        print(f'Order was saved {order}')

    def get_history(self):
        order = self.redis_client.get_order(RedisBridge.HISTORY)
        if not order:
            return
        action = 'Complete' if order['success'] else 'Created'
        History.objects.create(username=order['user'], order=order, action=action)
        print(f'History record was saved {order}')

    def handle(self, *args, **options):
        self.signal_register()

        while True:
            self.get_notification()
            self.get_history()

            print(f'Loop done')
            time.sleep(5)
