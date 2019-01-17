from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


# from django.conf import settings


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
    modalities = models.ManyToManyField('Modality')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf', 'date_of_birth']

    def __str__(self):
        return self.name


class Modality(models.Model):
    """Create and save new modality"""
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=1)
    fee = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Event(models.Model):
    """Create and save Event"""
    name = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    price = models.FloatField()
    modalities = models.ManyToManyField('Modality')

    def __str__(self):
        return self.name


class Product(models.Model):
    """Create and save Products"""
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=280)
    amount = models.IntegerField()
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=140)
    event = models.ForeignKey('Event', on_delete=models.CASCADE,)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Bought(models.Model):
    """Create and save Bought"""
    price = models.FloatField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE,)

    def __str__(self):
        return self.price


class Voucher(models.Model):
    """Create and save Model"""
    price = models.FloatField()
    amount = models.IntegerField()
    lot = models.IntegerField()
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.price)


class Transaction(models.Model):
    """Create a intermediate table for sale and product"""
    amount = models.FloatField()
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class Packet(models.Model):
    """Create a intermadiate table for sale and voucher"""
    amount = models.FloatField()
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    voucher = models.ForeignKey('Voucher', on_delete=models.CASCADE)


class Sale(models.Model):
    """Create and save sales"""
    products = models.ManyToManyField('Product', through='Transaction')
    vouchers = models.ManyToManyField('Voucher', through='Packet')
    value = models.FloatField(default=0)
    discount = models.FloatField()
    taxes = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    empl = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='empl')
    buyer = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.value)
