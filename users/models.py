from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django_countries.fields import CountryField

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [
        ('Admin', 'Admin'),
        ('Customer', 'Customer'),
        ('CarOwner', 'Car Owner'),
    ]
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20, blank=False, null=False)
    country = CountryField(blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to='users/profile-images', null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, blank=False, null=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return self.email


