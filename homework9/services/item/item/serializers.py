from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        # Hack for save None value
        if not self.validated_data.get('username'):
            self.instance.username = None

        return super().save(**kwargs)

    class Meta:
        model = Item
        fields = ('username',)
