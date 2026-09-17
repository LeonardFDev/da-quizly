from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegistrationSerializer, LoginSerializer


def blacklist_old_refresh_token(request):
    refresh = request.COOKIES.get("refresh_token")

    if refresh:
        try:
            RefreshToken(refresh).blacklist()
        except TokenError:
            pass


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        blacklist_old_refresh_token(request)
        
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            serializer.save()
            data = {
                "detail": "User created successfully!"
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        blacklist_old_refresh_token(request)

        response = super().post(request, *args, **kwargs)
            
        refresh = response.data.get("refresh")
        access = response.data.get("access")

        user = response.data.get("user")

        response.set_cookie(
            key="access_token",
            value= access,
            httponly= True,
            secure= True,
            samesite="Lax"
        )

        response.set_cookie(
            key="refresh_token",
            value= refresh,
            httponly= True,
            secure= True,
            samesite="Lax"
        )

        response.data = {
            "detail": "Login successfully!",
            "user": user
        }
        return response


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        self.no_refresh_token_error(refresh_token)

        return self.update_access_token(refresh_token)

    def no_refresh_token_error(self, refresh_token):
        if refresh_token is None:
            raise NotAuthenticated("Refresh token not found!")

    def update_access_token(self, refresh_token):
        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception= True)
        except:
            self.refresh_token_invalid_error()

        return self.update_token_cookie(serializer)

    def refresh_token_invalid_error(self):
        raise NotAuthenticated("Refresh token invalid!")

    def update_token_cookie(self, serializer):
        access_token = serializer.validated_data.get("access")

        response = Response({"detail": "Token refreshed"})
        
        response.set_cookie(
            key="access_token",
            value= access_token,
            httponly= True,
            secure= True,
            samesite="Lax"
        )

        return response


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        try:
            if refresh_token:
                RefreshToken(refresh_token).blacklist()
        except TokenError:
            pass

        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."})

        response.delete_cookie(
            key="access_token",
            samesite="Lax"
        )

        response.delete_cookie(
            key="refresh_token",
            samesite="Lax"
        )

        return response
