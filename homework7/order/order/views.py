from rest_framework.generics import ListCreateAPIView

from .serializers import OrderSerializer


class OrderCreateListView(ListCreateAPIView):
    serializer_class = OrderSerializer
