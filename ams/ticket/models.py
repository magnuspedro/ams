from django.db import models
from uuid import uuid4
# Create your models here.


class Ticket(models.Model):
    """Create and save ticket"""
    code = models.CharField(max_length=255, default=uuid4())
    price = models.FloatField()
    lot = models.IntegerField()
    status = models.BooleanField(default=False)
    date = models.DateField()
    half = models.BooleanField(default=False)
    delegation = models.CharField(max_length=50)
    event = models.CharField(max_length=50)

    def __str__(self):
        return str(self.code)
