from rest_framework.generics import ListCreateAPIView

from .models import Notification
from .serializers import NotificationSerializer


class NotificationCreateListView(ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
