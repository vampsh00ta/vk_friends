from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Customer(AbstractUser):
    friends = models.ManyToManyField("Customer",blank=True)
    def __str__(self):
        return f"{self.id}"
