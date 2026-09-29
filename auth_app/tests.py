"""Tests for the authentication and registration API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from tests.helpers import status_code_with_message


class RegistrationTests(APITestCase):
    def test_registration_get_405(self):
        url = reverse("registration")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_registration_patch_405(self):
        url = reverse("registration")
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_registration_put_405(self):
        url = reverse("registration")
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            
    def test_registration_delete_405(self):
        url = reverse("registration")
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_registration_passwords_not_match_post_400(self):
        url = reverse("registration")
        data = {"username": "testuserTest", "email": "testuser@test.de", "password": "123456", "confirmed_password": "testpassword"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_valid_email_post_400(self):
        url = reverse("registration")
        data = {"username": "testuserTest", "email": "testuser.test.de", "password": "123456", "confirmed_password": "123456"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_double_profile_post_400(self):
        User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")

        url = reverse("registration")
        data = {"username": "testuserTest", "email": "testuser@test.de", "password": "123456", "confirmed_password": "123456"}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_post_201(self):
        url = reverse("registration")
        data = {"username": "testuserTest", "email": "testuser@test.de", "password": "123456", "confirmed_password": "123456"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTests(APITestCase):
    def test_login_get_405(self):
        url = reverse("login")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_login_patch_405(self):
        url = reverse("login")
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_login_put_405(self):
        url = reverse("login")
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
                    
    def test_login_delete_405(self):
        url = reverse("login")
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_login_unknown_username_post_401(self):
        User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
        
        url = reverse("login")
        data = {"username": "unknownUsername", "password": "123456"}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_wrong_password_post_401(self):
        User.objects.create_user(username="testuserTest", password="wrongPassword", email="testuser@test.de")
        
        url = reverse("login")
        data = {"username": "testuserTest", "password": "123456"}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_login_post_200(self):
        User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
    
        url = reverse("login")
        data = {"username": "testuserTest", "password": "123456"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogoutTests(APITestCase):
    def customized_setUp(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_logout_get_405(self):
        self.customized_setUp()

        url = reverse("logout")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_logout_patch_405(self):
        self.customized_setUp()

        url = reverse("logout")
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_logout_put_405(self):
        self.customized_setUp()

        url = reverse("logout")
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
                    
    def test_logout_delete_405(self):
        self.customized_setUp()

        url = reverse("logout")
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_logout_post_401(self):
        User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
        
        url = reverse("logout")
        response = self.client.post(url)
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_logout_about_bearer_post_200(self):
        self.customized_setUp()

        url = reverse("logout")
        response = self.client.post(url)

        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_about_cookies_post_200(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        self.client.cookies["access_token"] = str(access)
        self.client.cookies["refresh_token"] = str(refresh)
    
        url = reverse("logout")
        response = self.client.post(url)

        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TokenRefreshTests(APITestCase):
    def customized_setUp(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
        
        self.refresh = RefreshToken.for_user(user)
        access = self.refresh.access_token

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_token_refresh_get_405(self):
        self.customized_setUp()

        url = reverse("token_refresh")
        response = self.client.get(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_token_refresh_patch_405(self):
        self.customized_setUp()

        url = reverse("token_refresh")
        response = self.client.patch(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_token_refresh_put_405(self):
        self.customized_setUp()

        url = reverse("token_refresh")
        response = self.client.put(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
                    
    def test_token_refresh_delete_405(self):
        self.customized_setUp()

        url = reverse("token_refresh")
        response = self.client.delete(url)

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_token_refresh_post_401(self):
        User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
        
        url = reverse("token_refresh")
        response = self.client.post(url)
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_token_refresh_about_bearer_post_200(self):
        self.customized_setUp()
        self.client.cookies["refresh_token"] = str(self.refresh)

        url = reverse("token_refresh")
        response = self.client.post(url)

        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh_about_cookies_post_200(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        self.client.cookies["access_token"] = str(access)
        self.client.cookies["refresh_token"] = str(refresh)
    
        url = reverse("token_refresh")
        response = self.client.post(url)

        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)