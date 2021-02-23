from django.db import models


class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    username = models.CharField(max_length=32)
    message = models.TextField()
    success = models.BooleanField()


class History(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    username = models.CharField(max_length=32)
    action = models.CharField(max_length=32)
    order = models.JSONField()
