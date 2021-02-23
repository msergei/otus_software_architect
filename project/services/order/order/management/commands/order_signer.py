import time

from order.redis import RedisBridge
from order.base import Signals


class Command(Signals):
    help = 'Order signer - blockchain imitation'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MATCH_PAIRS = {}
        self.redis_client = RedisBridge()

    def get_orders(self):
        orders = self.redis_client.get_order(RedisBridge.ORDERS_TO_SIGN)
        if orders:
            order_from, order_to = orders

            # Create transactions and get confirmation...

            order_from['success'] = True
            order_to['success'] = True

            print(f'Orders were signed: {orders}')
            return orders

    def handle(self, *args, **options):
        self.signal_register()

        while True:
            orders = self.get_orders()
            if orders:
                self.redis_client.publish_orders(orders, (
                    RedisBridge.COMPLETED_ORDERS,
                    RedisBridge.HISTORY,
                    RedisBridge.NOTIFY,
                ))
            time.sleep(5)
            print('Loop done')
