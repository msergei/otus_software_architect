import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.status import HTTP_201_CREATED
from rest_framework.exceptions import  APIException


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        response = requests.post(
            settings.BILLING_URL,
            data={
                'username': instance.username,
                'wallet': 100,
                'email': instance.email,
            }
        )
        if response.status_code != HTTP_201_CREATED:
            raise APIException(f'Billing account creation fail for {instance}: {response.text}')
