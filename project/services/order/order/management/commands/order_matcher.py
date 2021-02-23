import sys
import json
import time
import signal

from django.core.management.base import BaseCommand
from django.conf import settings
from rest_framework import status

from order.models import Order
from django.db import transaction
from json import dumps
from django.forms.models import model_to_dict
import redis
from order.redis import RedisBridge
from order.base import Signals


class Command(Signals):
    help = 'Order mather'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MATCH_PAIRS = {}
        self.redis_client = RedisBridge()

    def get_orders_for_match(self):
        data = self.redis_client.get_order_unique()

        while data:
            currency_from = data['currency_from']
            currency_to = data['currency_to']
            self.MATCH_PAIRS.setdefault(f'{currency_from}-{currency_to}', []).append(data)

            print(f'Got for match {data}')
            data = self.redis_client.get_order_unique()

    def match(self):
        pairs = tuple(self.MATCH_PAIRS.keys())

        for pair in pairs:
            orders_from = self.MATCH_PAIRS[pair]

            for i, order_from in enumerate(orders_from):
                currency_from = order_from['currency_from']
                currency_to = order_from['currency_to']
                title_pair_to = f'{currency_to}-{currency_from}'

                orders_to = self.MATCH_PAIRS.setdefault(title_pair_to, [])

                for j, order_to in enumerate(orders_to):

                    if order_to['amount'] == order_from['amount']:
                        # Let's match orders
                        orders_to.pop(j)
                        orders_from.pop(i)

                        self.redis_client.orders_to_sign(order_from, order_to)

                        print(f'Matched orders: {orders_from}<<>>{order_to}')

    def handle(self, *args, **options):
        self.signal_register()

        while True:
            self.get_orders_for_match()
            self.match()
            time.sleep(5)
            print('Loop done')
