from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@test', password='1245', cpf='12312312323',
                date_of_birth='2017-10-10'):
    """Create sample user"""
    return get_user_model().objects.create_user(email=email, password=password,
                                                cpf=cpf,
                                                date_of_birth=date_of_birth)


class ModelTests(TestCase):

    def test_create_user_with_email_sucessful(self):
        """Test creating a new user with an email"""
        email = "test@test.com"
        password = "Testpass123"
        cpf = "123453"
        date_of_birth = "1997-10-03"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            cpf=cpf,
            date_of_birth=date_of_birth
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email mormalized"""
        email = "test@TEST.COM"
        cpf = "123453"
        date_of_birth = "1997-10-03"
        user = get_user_model().objects.create_user(
            email=email,
            password='123443',
            cpf=cpf,
            date_of_birth=date_of_birth
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test createing user with no email raises error"""
        with self.assertRaises(ValueError):
            cpf = "123453"
            date_of_birth = "1997-10-03"
            get_user_model().objects.create_user(
                None,
                password='123443',
                cpf=cpf,
                date_of_birth=date_of_birth
            )

    def test_new_user_invalid_cpf(self):
        """Test createing user with no cpf raises error"""
        with self.assertRaises(ValueError):
            email = "test@test.com"
            date_of_birth = "1997-10-03"
            get_user_model().objects.create_user(
                email=email,
                password='123443',
                cpf=None,
                date_of_birth=date_of_birth
            )

    def test_new_user_invalid_date_of_birth(self):
        """Test createing user with no email raises error"""
        with self.assertRaises(ValueError):
            email = "test@test.com"
            cpf = "123453"
            get_user_model().objects.create_user(
                email=email,
                password='123443',
                cpf=cpf,
                date_of_birth=None
            )

    def test_create_new_superuser(self):
        """Test creating a new super user"""
        email = "test@test.com"
        cpf = "123453"
        date_of_birth = "1997-10-03"

        user = get_user_model().objects.create_superuser(
            email=email,
            password='123443',
            cpf=cpf,
            date_of_birth=date_of_birth
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_modality_str(self):
        """Test the modality string representation"""
        modality = models.Modality.objects.create(
            name='Basquete',
            sex='M',
            fee=10.0,
        )

        self.assertEqual(str(modality), modality.name)

    def test_event_str(self):
        """Test the event string representation"""
        event = models.Event.objects.create(
            name='JOIA',
            start='2018-10-10',
            end='2018-11-11',
            price=10.00,
        )

        self.assertEqual(str(event), event.name)
