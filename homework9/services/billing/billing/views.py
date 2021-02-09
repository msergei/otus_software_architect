from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from .models import UserProfile
from .serializers import UserBillingSerializer


class UserAccountCreateView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserBillingSerializer


class UserAccountDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserBillingSerializer
