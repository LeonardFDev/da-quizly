"""URL configuration for the register, login, logout and token refresh API."""

from django.urls import path

from .views import RegistrationView, LoginView, LogoutView, CustomTokenRefreshView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]