from django.db import models


class Notification(models.Model):
    email = models.EmailField()
    message = models.TextField()
    success = models.BooleanField()
