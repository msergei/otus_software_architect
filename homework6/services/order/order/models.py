from django.db import models


class Order(models.Model):
    username = models.CharField(max_length=150)
    amount = models.FloatField()
    details = models.JSONField()

    def __str__(self):
        return f'{self.username} order {self.id}'
