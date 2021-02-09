from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import OrderCreateListView

urlpatterns = [
    path("api/orders/", OrderCreateListView.as_view(), name="orders"),
]
