"""
This module contains models related to User Model.

Author: Natnael
Date: 01/04/2023
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
import uuid
from django.dispatch import receiver

# Create your models here.


class UserManager(BaseUserManager):

    """Custom user manager for managing users"""

    def create_user(self, email, password=None):
        """Create and save a new user with given email and password."""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser or admin user with given email and password."""
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """Custom user model with email & password authentication."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField('Email', unique=True)
    is_active = models.BooleanField('IsActive', default=True)
    is_admin = models.BooleanField('IsAdmin', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
