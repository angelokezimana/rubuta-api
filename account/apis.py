from rest_framework import views, response, exceptions, permissions, status

from .models import User
from .serializers import UserSerializer, ChangePasswordSerializer
from . import services, auth, permissions as custom_permissions


class RegisterApi(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        serializer.instance = services.create_user(user=data)

        return response.Response(data=serializer.data)


class LoginApi(views.APIView):
    authentication_classes = (auth.CustomUserAuth,)
    permission_classes = (custom_permissions.IsNotAuthenticated,)

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        token = services.create_token(user_id=user.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


class UserApi(views.APIView):
    authentication_classes = (auth.CustomUserAuth,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)

        return response.Response(serializer.data)


class LogoutApi(views.APIView):
    authentication_classes = (auth.CustomUserAuth,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "logout"}

        return resp


class ChangePasswordApi(views.APIView):
    authentication_classes = (auth.CustomUserAuth,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = request.user

        user.set_password(data["password"])

        user.save()

        return response.Response(
            {"message": "Password changed successfully!"}, status=status.HTTP_200_OK
        )
