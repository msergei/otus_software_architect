from rest_framework import serializers

from .models import Notification, History


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'
