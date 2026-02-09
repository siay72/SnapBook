from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    LOCATION_CHOICES = [
        ('Dhaka', 'Dhaka'),
        ('Chittagong', 'Chittagong'),
        ('Khulna', 'Khulna'),
        ('Rajshahi', 'Rajshahi'),
        ('Barisal', 'Barisal'),
        ('Sylhet', 'Sylhet'),
        ('Rangpur', 'Rangpur'),
        ('Mymensingh', 'Mymensingh'),
    ]
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'  # Use email instead of username
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


