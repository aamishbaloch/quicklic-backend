from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from libs.factories import PatientFactory, DoctorFactory, AdminFactory
from libs.factories import FACTORY_USER_PASSWORD
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientRegistrationAPITests(APITestCase):

    def test_create_patient(self):
        """
        Ensure we can create a new patient object.
        """
        url = reverse('register')

        patient = PatientFactory.build()
        patient_dict = {
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'email': patient.email,
            'password': FACTORY_USER_PASSWORD,
        }

        response = self.client.post(url, patient_dict, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], patient_dict['email'])
        self.assertEqual(response.data['role'], User.Role.PATIENT)

    def test_patient_already_exists(self):
        """
        Ensure we can't have duplicate emails.
        """
        url = reverse('register')

        patient = PatientFactory.create()
        patient_dict = {
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'email': patient.email,
            'password': FACTORY_USER_PASSWORD,
        }

        response = self.client.post(url, patient_dict, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginAPITests(APITestCase):

    def test_login_patient(self):
        """
        Ensure we can login with a valid patient.
        """
        patient = PatientFactory.create()
        url = reverse('login')
        data = {
            "email": patient.email,
            "password": FACTORY_USER_PASSWORD,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_patient_credentials(self):
        """
        Ensure we can't login with invalid credentials.
        """
        patient = PatientFactory.create()
        url = reverse('login')
        data = {
            "email": patient.email,
            "password": FACTORY_USER_PASSWORD + "dummy",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_token(self):
        """
        Ensure we can login with a valid patient.
        """
        patient = PatientFactory.create()
        url = reverse('login')
        data = {
            "email": patient.email,
            "password": FACTORY_USER_PASSWORD,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_doctor(self):
        """
        Ensure we can login with a valid doctor.
        """
        doctor = DoctorFactory.create()
        url = reverse('login')
        data = {
            "email": doctor.email,
            "password": FACTORY_USER_PASSWORD,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_admin(self):
        """
        Ensure we can login with a valid admin.
        """
        admin = AdminFactory.create()
        url = reverse('login')
        data = {
            "email": admin.email,
            "password": FACTORY_USER_PASSWORD,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
