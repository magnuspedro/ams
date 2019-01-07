from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Event

from event.serializers import EventSerializer


EVENTS_URL = reverse('event:event-list')


def sample_event(**params):
    """Create and return event sample"""
    defaults = {
        'name': 'JOIA',
        'start': '2018-10-10',
        'end': '2018-11-11',
        'price': 10.00,
    }
    defaults.update(params)

    return Event.objects.create(**defaults)


class PublicEventApiTest(TestCase):
    """Test unauthenticade modality API acess"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test authentication is requeired"""
        res = self.client.get(EVENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEventApiTest(TestCase):
    """Test authenticade API acecss"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="normal@normal.com",
            password="1234",
            cpf="12342314",
            date_of_birth="1997-11-03"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_events(self):
        """Test retrieving list of events"""
        sample_event()
        sample_event()

        res = self.client.get(EVENTS_URL)

        events = Event.objects.all().order_by('-name')
        serializers = EventSerializer(events, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializers.data)

    def test_create_event_successful(self):
        """Test creating a new event"""
        payload = {
            'name': 'JOIA',
            'start': '2018-10-10',
            'end': '2018-11-11',
            'price': 10.00,
        }
        self.client.post(EVENTS_URL, payload)

        exists = Event.objects.filter(
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_event_invalid(self):
        """Test creating a new event with invalid payload"""
        payload = {
            'name': '',
            'start': '2018-10-10',
            'end': '2018-11-11',
            'price': 10.00,
        }
        res = self.client.post(EVENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
