from django.db import models
from django.core.validators import RegexValidator

PHONE_REGEXP = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                              message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class User(models.Model):
    username = models.CharField(max_length=12)

    name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)

    phone = models.CharField(validators=[PHONE_REGEXP], max_length=17, blank=True, null=True)
    email = models.EmailField(max_length=128, blank=True, null=True)
