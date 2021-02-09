from django.db import models


class Slot(models.Model):
    time = models.CharField(max_length=5, primary_key=True)
    username = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f'{self.time}'
