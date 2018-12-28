from django.test import TestCase
from django.contrib.auth import get_user_model


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
