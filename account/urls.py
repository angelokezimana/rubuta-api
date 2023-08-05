from django.urls import path

from . import apis

urlpatterns = [
    path("jwt/delete/", apis.LogoutApi.as_view(), name="logout"),
]
