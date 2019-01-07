from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Modality

from modality.serializers import ModalitySerializer


MODALITIES_URL = reverse('modality:modality-list')


def sample_modality(**params):
    """Create and return a sample modality"""
    defaults = {
        'name': 'Basquete',
        'fee': 10,
        'sex': 'M',
    }
    defaults.update(params)

    return Modality.objects.create(**defaults)


class PublicModalityApiTests(TestCase):
    """Test unauthenticated modality API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(MODALITIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateModalityApiTests(TestCase):
    """Test authenticated modality API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="normal@normal.com",
            password="1234",
            cpf="12342314",
            date_of_birth="1997-11-03"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_modalities(self):
        """Test retrieving list of modalities"""
        sample_modality()
        sample_modality()

        res = self.client.get(MODALITIES_URL)

        modalities = Modality.objects.all().order_by('-name')
        serializer = ModalitySerializer(modalities, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
