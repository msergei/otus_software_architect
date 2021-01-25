import requests
from django.conf import settings
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from .permissions import UsernameExisted
from .models import Order
from .serializers import OrderSerializer


class OrderCreateListView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (UsernameExisted,)

    def get(self, request, *args, **kwargs):
        self.queryset = Order.objects.filter(username=request.username)
        return super().get(request, *args, **kwargs)

    @staticmethod
    def send_notification(email, message, success):
        response = requests.post(settings.NOTIFY_URL,
                                 data={'email': email, 'message': message, 'success': success})

        if response.status_code != status.HTTP_201_CREATED:
            raise APIException('Notification error occurred, please try later')

        print(f'Notification added {email} {message}')

    def post(self, request, *args, **kwargs):
        user_id_field = settings.SIMPLE_JWT['USER_ID_FIELD']
        request.data[user_id_field] = request.username

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        response = requests.get(f'{settings.BILLING_URL}/{request.username}',
                                headers={'Authorization': request.headers['Authorization']})

        if response.status_code != status.HTTP_200_OK:
            return Response('User does not exist', status=status.HTTP_404_NOT_FOUND)

        account = response.json()
        wallet = account['wallet']
        email = account['email']

        if wallet < data['amount']:
            message = f'Not enough money to create order with amount {data["amount"]}: {data["details"]}'
            self.send_notification(email, message, False)
            return Response({'error': True, 'details': message}, status=status.HTTP_400_BAD_REQUEST)

        wallet -= data['amount']
        response = requests.patch(f'{settings.BILLING_URL}/{request.username}', data={'wallet': wallet},
                                  headers={'Authorization': request.headers['Authorization']})

        if response.status_code != status.HTTP_200_OK:
            message = f'Order with amount {data["amount"]} {data["details"]} did not create, details: {response.text}'
            self.send_notification(email, message, False)
            return Response(response.json(), status=response.status_code)

        self.perform_create(serializer)
        message = f'Order {data["amount"]} {data["details"]} was created'
        self.send_notification(email, message, True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
