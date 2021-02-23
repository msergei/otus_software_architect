import time

from order.models import Order, Wallet
from django.db import transaction

from order.redis import RedisBridge
from order.base import Signals


class Command(Signals):
    help = 'Order SAGA mediator'

    @transaction.atomic
    def init_orders(self, redis_client):
        orders = Order.objects.filter(published=False).select_for_update()
        redis_client.publish_orders(orders, (RedisBridge.ORDERS, RedisBridge.HISTORY))
        orders.update(published=True)

    def get_completed_orders(self, redis_client):
        """Get orders for complete"""

        orders = []
        data = redis_client.get_order(RedisBridge.COMPLETED_ORDERS)
        while data:
            orders.append(data)
            data = redis_client.get_order(RedisBridge.COMPLETED_ORDERS)

        print(f'Got {orders} for complete')

        ids = []
        for order in orders:
            wallet, created = Wallet.objects.get_or_create(user_id=order['user'], currency_id=order['currency_to'])
            wallet.wallet += order['amount']
            wallet.save()
            ids.append(order['id'])

        Order.objects.filter(id__in=ids).update(success=True)

    def handle(self, *args, **options):
        self.signal_register()
        redis_client = RedisBridge()

        while True:
            self.init_orders(redis_client)
            self.get_completed_orders(redis_client)
            time.sleep(5)
