from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from entities.profile_item.models import DoctorProfile
from libs.factories import DoctorFactory, PatientFactory
from libs.factories import FACTORY_USER_PASSWORD
from django.contrib.auth import get_user_model

User = get_user_model()


class DoctorViewAPITests(APITestCase):

    def setUp(self):
        patient = PatientFactory.create()
        url = reverse('login')
        data = {
            "email": patient.email,
            "password": FACTORY_USER_PASSWORD,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        self.token = response.data['token']

    def test_doctors_list(self):
        """
        Ensure we can get a list of all doctors
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        DoctorFactory.create_batch(5)
        url = reverse('doctor-all')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_active_doctors_list_only(self):
        """
        Ensure we can get a list of all Active doctors only
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        DoctorFactory.create_batch(5, is_active=False)
        url = reverse('doctor-all')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_active_doctors_list_visible_to_active_patients(self):
        """
        Ensure inactive patient can't get a list of all doctors
        """
        patient = PatientFactory.create(is_active=False)
        self.client.force_authenticate(user=patient)
        DoctorFactory.create_batch(5)
        url = reverse('doctor-all')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_active_doctors_list_invisible_to_doctor(self):
        """
        Ensure doctor can't get a list of all doctors
        """
        doctor = DoctorFactory.create()
        self.client.force_authenticate(user=doctor)
        DoctorFactory.create_batch(5, is_active=False)
        url = reverse('doctor-all')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
