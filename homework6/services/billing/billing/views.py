from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
from .permissions import IsOwnerProfile
from .serializers import UserBillingSerializer


class UserAccountCreateView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserBillingSerializer


class UserAccountDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserBillingSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfile]
