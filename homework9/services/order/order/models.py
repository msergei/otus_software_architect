from django.db import models


class Order(models.Model):
    username = models.CharField(max_length=150)
    amount = models.FloatField()
    details = models.JSONField()
    success = models.BooleanField(null=True, blank=True)
    reason = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.username} order {self.id}'
