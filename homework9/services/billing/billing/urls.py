from django.urls import path

from .views import UserAccountCreateView, UserAccountDetailView

urlpatterns = [
    path("api/profiles/", UserAccountCreateView.as_view(), name="all-profiles"),
    path("api/accounts/<str:pk>", UserAccountDetailView.as_view(), name="profile")
]
