from django.urls import path

from .views import ItemReserveView, ItemCancelView

urlpatterns = [
    path("api/items/reserve/<int:pk>", ItemReserveView.as_view(), name="reserve-item"),
    path("api/items/cancel/<int:pk>", ItemCancelView.as_view(), name="cancel-reserve"),
]
