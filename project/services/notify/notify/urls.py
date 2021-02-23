from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import NotificationListView, HistoryListView

from rest_framework import permissions


urlpatterns = [
    path("api/notifications/", NotificationListView.as_view(), name="orders"),
    path("api/history/", HistoryListView.as_view(), name="orders"),
]
