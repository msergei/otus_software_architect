import json
from django.conf import settings
from django.forms.models import model_to_dict
from django.db import transaction

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from .permissions import UsernameExisted
from .models import Order
from .serializers import OrderSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile, Currency, Wallet
from .permissions import IsOwner
from .serializers import UserBillingSerializer, CurrencySerializer, WalletSerializer


class OrderCreateListView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsOwner,)

    def get(self, request, *args, **kwargs):
        self.queryset = Order.objects.filter(user=request.user)
        return super().get(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)

        wallet = serializer.validated_data.pop('wallet')
        wallet.save()

        serializer.save(user=self.request.user)

        return Response({'success': True}, status=status.HTTP_201_CREATED)


class WalletCreateListView(ListCreateAPIView, RetrieveUpdateAPIView):
    serializer_class = WalletSerializer
    permission_classes = (IsOwner,)

    def get(self, request, *args, **kwargs):
        self.queryset = Wallet.objects.filter(user=request.user)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response({'success': True}, status=status.HTTP_201_CREATED)


class UserAccountCreateView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserBillingSerializer


class UserAccountDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserBillingSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class CurrencyView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

