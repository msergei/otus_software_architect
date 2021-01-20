from django.contrib import admin
from django.urls import path

from .views import UserProfileListCreateView, UserProfileDetailView

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/internal/profiles/", UserProfileListCreateView.as_view(), name="all-profiles"),
    path("api/profiles/<str:pk>", UserProfileDetailView.as_view(), name="profile")

]
