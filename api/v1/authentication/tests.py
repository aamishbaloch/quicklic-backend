from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationAPITests(APITestCase):

    def setUp(self):

        self.user_dict = {
            'first_name': 'aamish',
            'last_name': 'baloch',
            'email': 'aamish@gmail.com',
            'password': 'githubisawesome',
        }

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('register')
        data = self.user_dict
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], self.user_dict['email'])

    def test_username_already_exists(self):
        """
        Ensure we can't have duplicate usernames.
        """
        url = reverse('register')

        serializer = UserSerializer(data=self.user_dict)
        if serializer.is_valid():
            serializer.save()

        response = self.client.post(url, self.user_dict, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_patient(self):
        """
        Ensure we can create a new patient object.
        """
        url = reverse('register')
        data = self.user_dict
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], self.user_dict['email'])
        self.assertEqual(response.data['role'], User.Role.PATIENT)


class UserLoginAPITests(APITestCase):

    def setUp(self):

        self.user_dict = {
            'first_name': 'aamish',
            'last_name': 'baloch',
            'email': 'aamish@gmail.com',
            'password': 'githubisawesome',
        }

        serializer = UserSerializer(data=self.user_dict)
        if serializer.is_valid():
            serializer.save()

    def test_login_user(self):
        """
        Ensure we can login with a valid user.
        """
        url = reverse('login')
        data = {
            "email": self.user_dict['email'],
            "password": self.user_dict['password'],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_credentials(self):
        """
        Ensure we can't login with invalid credentials.
        """
        url = reverse('login')
        data = {
            "email": self.user_dict['email'],
            "password": 'pythonisawesome',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
