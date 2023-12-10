from account.models import User
from account.permissions import UserOrGroupPermissions
from account.serializers import ContentTypeSerializer
from account.serializers import GroupSerializer
from account.serializers import UserSerializer
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutApi(APIView):
    """
    Send a JSON object with:
        - refresh_token in post data when we want to blacklist
            the current refresh_token;
        - all in post data when we want to blacklist
            all refresh_tokens for the current user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if self.request.data.get("all"):
            # token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)

            return Response(status=status.HTTP_205_RESET_CONTENT)

        try:
            refresh_token = self.request.data.get("refresh_token")
            token = RefreshToken(token=refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GroupListApi(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & UserOrGroupPermissions]

    required_permissions = {"GET": ["view_group"], "POST": ["add_group"]}

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDetailApi(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & UserOrGroupPermissions]

    required_permissions = {
        "GET": ["view_group"],
        "PUT": ["change_group"],
        "DELETE": ["delete_group"],
    }

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserListApi(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & UserOrGroupPermissions]

    required_permissions = {"GET": ["view_user"], "POST": ["add_user"]}

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailApi(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update user details
    """

    permission_classes = [IsAuthenticated & UserOrGroupPermissions]

    required_permissions = {"GET": ["view_user"], "PUT": ["change_user"]}

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PermissionListApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    not_contenttypes = ~Q(app_label="contenttypes")
    not_admin = ~Q(app_label="admin")
    not_sessions = ~Q(app_label="sessions")
    not_token_blacklist = ~Q(app_label="token_blacklist")

    queryset = ContentType.objects.filter(
        not_contenttypes & not_admin & not_sessions & not_token_blacklist
    )
    serializer_class = ContentTypeSerializer
