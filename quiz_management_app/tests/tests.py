"""Tests for the logout API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from tests.helpers import status_code_with_message
from .data import quizzes_data


class QuizzesPutTests(APITestCase):
    def customized_setUp(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        self.client.cookies["access_token"] = str(access)
        self.client.cookies["refresh_token"] = str(refresh)
        
    def test_quizzes_put_405(self):
        self.customized_setUp()

        url = reverse("quiz-list")
        data = {"url": "https://youtu.be/mR1fpuZjFRw?si=T7II-otDXIrDoiVg"}
        response = self.client.put(url, data, format= "json")

        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class QuizzesPostTests(APITestCase):
    def customized_setUp(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
            
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
            
        self.client.cookies["access_token"] = str(access)
        self.client.cookies["refresh_token"] = str(refresh)

    def test_quizzes_url_without_audio_post_400(self):
        self.customized_setUp()

        url = reverse("quiz-list")
        data = {"url": "https://www.google.com/"}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_quizzes_without_url_post_400(self):
        self.customized_setUp()

        url = reverse("quiz-list")
        data = {"url": ""}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_quizzes_post_401(self):
        User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
        
        url = reverse("quiz-list")
        data = {"url": "https://youtu.be/mR1fpuZjFRw?si=T7II-otDXIrDoiVg"}
        response = self.client.post(url, data, format= "json")
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_quizzes_about_bearer_post_201(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        url = reverse("quiz-list")
        data = {"url": "https://youtu.be/mR1fpuZjFRw?si=T7II-otDXIrDoiVg"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_quizzes_about_cookies_post_201(self):
        self.customized_setUp()
    
        url = reverse("quiz-list")
        data = {"url": "https://youtu.be/mR1fpuZjFRw?si=T7II-otDXIrDoiVg"}
        response = self.client.post(url, data, format= "json")

        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class QuizzesGetListTests(APITestCase):
    def customized_setUp(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
            
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
            
        self.client.cookies["access_token"] = str(access)
        self.client.cookies["refresh_token"] = str(refresh)

        quizzes_data(user)

    def test_quizzes_get_list_401(self):
        User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
        
        url = reverse("quiz-list")
        response = self.client.get(url)
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_quizzes_about_bearer_get_list_200(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        quizzes_data(user)

        url = reverse("quiz-list")
        response = self.client.get(url)

        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_quizzes_about_cookies_get_list_200(self):
        self.customized_setUp()
    
        url = reverse("quiz-list")
        response = self.client.get(url)

        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_quizzes_empty_list_get_list_200(self):
        user = User.objects.create_user(username="testuserTest3", password="123456", email="testuser3@test.de")
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        
        url = reverse("quiz-list")
        response = self.client.get(url)
    
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuizzesGetRetrieveTests(APITestCase):
    def customized_setUp(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
    
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
    
        self.client.cookies["access_token"] = str(access)
        self.client.cookies["refresh_token"] = str(refresh)
    
        quizzes_data(user)
    
    def test_quizzes_get_retrieve_401(self):
        url = reverse("quiz-detail", kwargs={"pk": 1})
        response = self.client.get(url)
    
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_quizzes_get_retrieve_403(self):
        self.customized_setUp()
        
        url = reverse("quiz-detail", kwargs={"pk": 4})
        response = self.client.get(url)
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_quizzes_get_retrieve_404(self):
        self.customized_setUp()
        
        url = reverse("quiz-detail", kwargs={"pk": 999})
        response = self.client.get(url)
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_quizzes_about_bearer_get_retrieve_200(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
    
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
    
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    
        quizzes_data(user)
    
        url = reverse("quiz-detail", kwargs={"pk": 1})
        response = self.client.get(url)
    
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_quizzes_about_cookies_get_retrieve_200(self):
        self.customized_setUp()
    
        url = reverse("quiz-detail", kwargs={"pk": 1})
        response = self.client.get(url)
    
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuizzesPatchTests(APITestCase):
    def customized_setUp(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
    
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
    
        self.client.cookies["access_token"] = str(access)
        self.client.cookies["refresh_token"] = str(refresh)
    
        quizzes_data(user)

    def test_quizzes_patch_400(self):
        self.customized_setUp()

        url = reverse("quiz-detail", kwargs={"pk": 1})
        data = {"title": "", "description": ""}
        response = self.client.patch(url, data, format= "json")
        
        status_code_with_message(self, response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_quizzes_patch_401(self):
        url = reverse("quiz-detail", kwargs={"pk": 1})
        data = {"title": "Partially Updated Title", "description": "Partially Updated Description"}
        response = self.client.patch(url, data, format= "json")
    
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_quizzes_patch_403(self):
        self.customized_setUp()
        
        url = reverse("quiz-detail", kwargs={"pk": 4})
        data = {"title": "Partially Updated Title", "description": "Partially Updated Description"}
        response = self.client.patch(url, data, format= "json")
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_quizzes_patch_404(self):
        self.customized_setUp()
        
        url = reverse("quiz-detail", kwargs={"pk": 999})
        data = {"title": "Partially Updated Title", "description": "Partially Updated Description"}
        response = self.client.patch(url, data, format= "json")
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_quizzes_about_bearer_patch_200(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
    
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
    
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    
        quizzes_data(user)
    
        url = reverse("quiz-detail", kwargs={"pk": 1})
        data = {"title": "Partially Updated Title", "description": "Partially Updated Description"}
        response = self.client.patch(url, data, format= "json")
    
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_quizzes_about_cookies_patch_200(self):
        self.customized_setUp()
    
        url = reverse("quiz-detail", kwargs={"pk": 1})
        data = {"title": "Partially Updated Title", "description": "Partially Updated Description"}
        response = self.client.patch(url, data, format= "json")
    
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuizzesDeleteTests(APITestCase):
    def customized_setUp(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
    
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
    
        self.client.cookies["access_token"] = str(access)
        self.client.cookies["refresh_token"] = str(refresh)
    
        quizzes_data(user)
    
    def test_quizzes_delete_401(self):
        url = reverse("quiz-detail", kwargs={"pk": 1})
        response = self.client.delete(url)
    
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_quizzes_patch_403(self):
        self.customized_setUp()
        
        url = reverse("quiz-detail", kwargs={"pk": 4})
        response = self.client.delete(url)
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_quizzes_delete_404(self):
        self.customized_setUp()
        
        url = reverse("quiz-detail", kwargs={"pk": 999})
        response = self.client.delete(url)
        
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_quizzes_about_bearer_delete_204(self):
        user = User.objects.create_user(username="testuserTest", password="123456", email="testuser@test.de")
    
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
    
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    
        quizzes_data(user)
    
        url = reverse("quiz-detail", kwargs={"pk": 1})
        response = self.client.delete(url)
    
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_quizzes_about_cookies_delete_204(self):
        self.customized_setUp()
    
        url = reverse("quiz-detail", kwargs={"pk": 1})
        response = self.client.delete(url)
    
        status_code_with_message(self, response) 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)