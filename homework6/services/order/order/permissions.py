from django.conf import settings
from rest_framework.permissions import BasePermission


class UsernameExisted(BasePermission):
    def has_permission(self, request, view):
        return bool(getattr(request, settings.SIMPLE_JWT['USER_ID_FIELD'], ''))

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
