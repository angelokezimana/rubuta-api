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

    permission_classes = (IsAuthenticated,)

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
