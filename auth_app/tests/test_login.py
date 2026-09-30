"""Tests for the authentication (login) API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from tests.helpers import status_code_with_message


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