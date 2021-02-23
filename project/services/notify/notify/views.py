from rest_framework.generics import ListAPIView

from .models import Notification, History
from .serializers import NotificationSerializer, HistorySerializer


class NotificationListView(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return super().get_queryset().filter(username=self.request.username)


class HistoryListView(ListAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def get_queryset(self):
        return super().get_queryset().filter(username=self.request.username)
