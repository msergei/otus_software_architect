import json
import redis
from django.conf import settings
from django.forms.models import model_to_dict

from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from .permissions import UsernameExisted
from .models import Order
from .serializers import OrderSerializer


class OrderCreateListView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (UsernameExisted,)

    def get(self, request, *args, **kwargs):
        self.queryset = Order.objects.filter(username=request.username)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_id_field = settings.SIMPLE_JWT['USER_ID_FIELD']
        request.data[user_id_field] = request.username

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        conn = redis.Redis(host=settings.REDIS_HOST, port=6379, db=0)
        conn.rpush(settings.ORDER_QUEUE, json.dumps(model_to_dict(instance)))

        return Response({'success': True}, status=status.HTTP_201_CREATED)
