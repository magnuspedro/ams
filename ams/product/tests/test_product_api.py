from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product, Event

from product.serializers import ProductSerializer

import sys

PRODUCT_URL = reverse('product:product-list')


def sample_product(event, **params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Sample product',
        'description': 'sample',
        'amount': 10,
        'size': 'Unico',
        'color': 'Unica',
        'price': 20,
    }
    defaults.update(params)

    return Product.objects.create(event=event, **defaults)


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


class PublicProductApiTest(TestCase):
    """Test the publicity available product API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrivng tags"""
        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductApiTest(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="normal@normal.com",
            password="1234",
            cpf="12342314",
            date_of_birth="1997-11-03"
        )
        self.client.force_authenticate(self.user)

    def test_retrive_products(self):
        """Test retriving products"""

        sample_product(event=sample_event())
        sample_product(event=sample_event())

        products = Product.objects.all().order_by('-name')
        res = self.client.get(PRODUCT_URL)
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_create_tag_successful(self):
    #     """Test creating a new tag"""
    #     payload = {
    #         'name': 'Sample product'
    #     }
    #     self.client.post(PRODUCT_URL, payload)
    #     exists = Product.objects.filter(
    #         name=payload['name']
    #     ).exists()

    #     self.assertTrue(exists)
