from django.urls import path

from account import apis


urlpatterns = [
    path("jwt/destroy/", apis.LogoutApi.as_view(), name="logout"),
    path("admin/groups/", apis.GroupListApi.as_view()),
    path("admin/groups/<int:pk>/", apis.GroupDetailApi.as_view(), name="groups"),
    path("admin/users/", apis.UserListApi.as_view()),
    path("admin/users/<int:pk>/", apis.UserDetailApi.as_view()),
    path("admin/permissions/", apis.PermissionListApi.as_view()),
]
