from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import OrderCreateListView, UserAccountCreateView, UserAccountDetailView, CurrencyView, WalletCreateListView


urlpatterns = [
    path("api/orders/", OrderCreateListView.as_view(), name="orders"),
    path("api/wallets/", WalletCreateListView.as_view(), name="wallets"),
    path("api/profiles/", UserAccountCreateView.as_view(), name="all-profiles"),
    path("api/currencies/", CurrencyView.as_view(), name="all-currencies"),
    path("api/accounts/<str:pk>", UserAccountDetailView.as_view(), name="profile")
]
