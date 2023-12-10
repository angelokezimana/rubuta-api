from django.contrib.auth.models import Permission
from rest_framework import permissions


class UserOrGroupPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        user_permissions = set(
            Permission.objects.filter(user=request.user).values_list(
                "codename", flat=True
            )
        )

        group_permissions = set(
            Permission.objects.filter(group__user=request.user).values_list(
                "codename", flat=True
            )
        )

        required_permissions_mapping = getattr(view, "required_permissions", {})

        required_permissions = set(required_permissions_mapping.get(request.method, []))

        if required_permissions.issubset(user_permissions | group_permissions):
            return True
        return False
