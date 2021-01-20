import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(f'Try to create profile {instance}')
        response = requests.post(settings.PROFILES_URL, data={'username': instance.username})
        print(f'Done {response}')
        # UserProfile.objects.create(user=instance)
