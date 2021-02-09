from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Slot
from .serializers import SlotSerializer


class SlotReserveView(RetrieveUpdateDestroyAPIView):
    queryset = Slot.objects.filter(username=None)
    serializer_class = SlotSerializer
