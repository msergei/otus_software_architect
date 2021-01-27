from django.urls import path

from .views import OrderCreateListView


urlpatterns = [
    path("api/orders/", OrderCreateListView.as_view(), name="orders"),
]
