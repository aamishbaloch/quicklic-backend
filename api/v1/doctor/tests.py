from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import DoctorSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class DoctorAPITests(APITestCase):

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
