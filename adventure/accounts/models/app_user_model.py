from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from adventure.accounts.managers import AppUserManger


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AppUserManger()

    def __str__(self):
        return self.email
