from django.urls import path

from .views import SlotReserveView

urlpatterns = [
    path("api/slots/reserve/<str:pk>", SlotReserveView.as_view(), name="reserve-slot"),
]
