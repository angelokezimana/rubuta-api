from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, ChangePasswordSerializer
from . import services


class RegisterApi(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        serializer.instance = services.create_user(user=data)

        return Response(data=serializer.data)


# class UserApi(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         user = request.user

#         serializer = UserSerializer(user)

#         return Response(serializer.data)


class LogoutApi(APIView):
    """
        Send a JSON object with:
            - refresh_token in post data when we want to blacklist the current refresh_token;
            - all in post data when we want to blacklist all refresh_tokens for the current user.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if self.request.data.get("all"):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)

            return Response(status=status.HTTP_205_RESET_CONTENT)

        try:
            refresh_token = self.request.data.get("refresh_token")
            token = RefreshToken(token=refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordApi(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = request.user

        user.set_password(data["password"])

        user.save()

        return Response(
            {"message": "Password changed successfully!"}, status=status.HTTP_200_OK
        )
