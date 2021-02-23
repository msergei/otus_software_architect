import json
import redis

from django.conf import settings
from django.forms.models import model_to_dict


class RedisBridge(object):
    ORDERS = 'orders'
    HISTORY = 'history'
    NOTIFY = 'notify'
    ORDERS_TO_SIGN = 'sign_orders'
    DONE_ORDERS_SET = 'done_orders'
    COMPLETED_ORDERS = 'completed_orders'

    def __init__(self):
        self.conn = redis.Redis(host=settings.REDIS_HOST, port=6379, db=0)

    def orders_to_sign(self, order_from, order_to):
        self.conn.rpush(self.ORDERS_TO_SIGN, json.dumps((order_from, order_to,)))
        self.conn.sadd(self.DONE_ORDERS_SET, order_from['id'], order_to['id'])

        return True

    def get_order_unique(self):
        # We need to get only unique orders
        data = self.conn.lpop(self.ORDERS)

        if data:
            order = json.loads(data)

            if not self.conn.sismember(self.DONE_ORDERS_SET, order['id']):
                return order

    def publish_orders(self, orders, queues):
        if not orders:
            return

        for order in orders:

            if not isinstance(order, dict):
                order = model_to_dict(order)
            for queue in queues:
                self.conn.rpush(queue, json.dumps(order))

        print(f'Published {orders} to queues')
        return True

    def get_order(self, queue):
        data = self.conn.lpop(queue)
        if data:
            order = json.loads(data)
            return order
