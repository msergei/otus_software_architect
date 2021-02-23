from django.conf import settings
from rest_framework import serializers, exceptions

from .models import Order, UserProfile, Currency, Wallet


class OrderSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        attrs = dict(super().validate(attrs))
        wallet = self.context.user.wallet_set.get(currency_id=attrs['currency_from'])

        wallet.wallet -= attrs['amount']
        wallet.wallet -= settings.SYSTEM_FEE
        if wallet.wallet < 0:
            raise exceptions.APIException('Not enough money')

        attrs['wallet'] = wallet
        return attrs

    class Meta:
        model = Order
        exclude = ('user', 'created_at')


class UserBillingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        exclude = ('wallets',)


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        exclude = ('user',)
