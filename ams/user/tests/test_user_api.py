from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class Public_user_ApiTest(TestCase):
    """Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_sucesss(self):
        """Test creating user with valid payload is sucessful"""
        payload = {
            'email': 'atletica@javas.com',
            'name': 'Atletica Javas',
            'password': 'chupa xv',
            'cpf': '12345678',
            'rg': '12344543',
            'phone': 'telefone allan',
            'course': 'Exatas',
            'sex': 'F',
            'date_of_birth': '2012-05-7'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'atletica@javas.com',
            'password': 'chupa xv',
            'name': 'Atletica Javas',
            'cpf': '12345678',
            'rg': '12344543',
            'phone': 'telefone allan',
            'course': 'Exatas',
            'sex': 'F',
            'date_of_birth': '2012-05-7'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 6 characters"""
        payload = {
            'email': 'atletica@javas.com',
            'name': 'Atletica Javas',
            'password': 'cpxv',
            'cpf': '12345678',
            'rg': '12344543',
            'phone': 'telefone allan',
            'course': 'Exatas',
            'sex': 'F',
            'date_of_birth': '2012-05-7'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email'],
                                                      cpf=payload['cpf'])
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is crated for the user"""
        payload = {
            'email': 'atletica@javas.com',
            'password': 'chupa xv',
            'cpf': '12345678',
            'date_of_birth': '2012-05-7'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid creadentials are given"""
        create_user(email='atletica@javas.com', password='javas e foda',
                    cpf='12345678', date_of_birth='2012-05-7')
        payload = {
            'email': 'atletica@javas.com',
            'password': 'chupa xv'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        payload = {
            'email': 'atletica@javas.com',
            'password': 'javas e foda'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are requierd"""
        payload = {
            'email': 'atletica@javas.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('toke', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
