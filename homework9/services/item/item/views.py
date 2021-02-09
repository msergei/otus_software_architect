from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Item
from .serializers import ItemSerializer
from rest_framework import status
from rest_framework.response import Response


class ItemReserveView(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.filter(username=None)
    serializer_class = ItemSerializer


class ItemCancelView(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.exclude(username=None)
    serializer_class = ItemSerializer
