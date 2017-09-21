from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from libs.factories import PatientFactory
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientRegistrationAPITests(APITestCase):

    def setUp(self):

        self.user_dict = {
            'first_name': PatientFactory.first_name,
            'last_name': PatientFactory.last_name,
            'email': PatientFactory.email,
            'password': 'githubisawesome'
        }

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

    def test_patient_already_exists(self):
        """
        Ensure we can't have duplicate emails.
        """
        url = reverse('register')

        PatientFactory.create()

        response = self.client.post(url, self.user_dict, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PatientLoginAPITests(APITestCase):

    def setUp(self):

        PatientFactory.create()

    def test_login_patient(self):
        """
        Ensure we can login with a valid patient.
        """
        url = reverse('login')
        data = {
            "email": PatientFactory.email,
            "password": 'githubisawesome',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_patient_credentials(self):
        """
        Ensure we can't login with invalid credentials.
        """
        url = reverse('login')
        data = {
            "email": PatientFactory.email,
            "password": 'pythonisawesome',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_token(self):
        """
        Ensure we can login with a valid patient.
        """
        url = reverse('login')
        data = {
            "email": PatientFactory.email,
            "password": 'githubisawesome',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
