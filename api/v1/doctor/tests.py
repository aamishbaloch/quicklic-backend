from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from libs.factories import DoctorFactory
from django.contrib.auth import get_user_model

User = get_user_model()


class DoctorAPITests(APITestCase):

    def test_doctors_list(self):
        """
        Ensure we can get a list of all doctors
        """
        DoctorFactory.create_batch(5)
        url = reverse('doctor-all')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_active_doctors_list_only(self):
        """
        Ensure we can get a list of all Active doctors only
        """
        DoctorFactory.create_batch(5, is_active=False)
        url = reverse('doctor-all')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
