"""register, login, logout and token refresh API views."""

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
    """Blacklist the refresh token"""

    refresh = request.COOKIES.get("refresh_token")

    if refresh:
        try:
            RefreshToken(refresh).blacklist()
        except TokenError:
            pass


class RegistrationView(APIView):
    """Provides an API endpoint for user registration."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user."""

        blacklist_old_refresh_token(request)
        
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            serializer.save()
            data = {
                "detail": "User created successfully!"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    """Provides an API endpoint for user authentication."""

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Authenticate the user and sets the tokens in cookie and outputs a confirmation as well as the user information"""
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
    """Provides an API endpoint for token refresh"""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """a new access token is created with the refresh token"""
        refresh_token = request.COOKIES.get("refresh_token")

        self.no_refresh_token_error(refresh_token)

        return self.update_access_token(refresh_token)

    def no_refresh_token_error(self, refresh_token):
        """Error creating a new token because there is no refresh token"""
        if refresh_token is None:
            raise NotAuthenticated("Refresh token not found!")

    def update_access_token(self, refresh_token):
        """try to generate a new access token"""
        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception= True)
        except:
            self.refresh_token_invalid_error()

        return self.update_token_cookie(serializer)

    def refresh_token_invalid_error(self):
        """Error message that the refresh token is no longer valid"""
        raise NotAuthenticated("Refresh token invalid!")

    def update_token_cookie(self, serializer):
        """Inserts the newly generated access token into the cookie"""
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
    """Provides an API endpoint for logout"""

    def post(self, request):
        """Blacklists the refresh_token and deletes the tokens from the cookies"""
        blacklist_old_refresh_token(request)

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
