from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=32)
    username = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f'{self.name} id {self.id}'
