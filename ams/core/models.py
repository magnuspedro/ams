from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        if not extra_fields['cpf']:
            raise ValueError('Users must have an cpf address')
        if not extra_fields['date_of_birth']:
            raise ValueError('Users must have an birth date address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, cpf, date_of_birth):
        """Create and saves new superuser"""
        user = self.create_user(email=email, password=password, cpf=cpf,
                                date_of_birth=date_of_birth)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Override the abstract method to use email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=15, unique=True)
    rg = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=30)
    is_partner = models.BooleanField(default=False)
    sex = models.CharField(max_length=1)
    date_of_birth = models.DateField()
    post = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf', 'date_of_birth']
