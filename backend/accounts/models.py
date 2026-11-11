from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError('Mobile number is required')
        user = self.model(mobile=mobile, username=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(mobile, password, **extra_fields)


class User(AbstractUser):
    LANGUAGE_CHOICES = [('en', 'English'), ('ta', 'Tamil'), ('hi', 'Hindi')]
    APP_LOCK_CHOICES = [('none', 'None'), ('pin', 'PIN'), ('biometric', 'Biometric')]

    mobile = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=120, blank=True)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    app_lock = models.CharField(max_length=10, choices=APP_LOCK_CHOICES, default='none')
    pin_hash = models.CharField(max_length=128, blank=True, null=True)
    auto_backup = models.BooleanField(default=True)
    last_backup_at = models.DateTimeField(blank=True, null=True)
    current_business = models.ForeignKey(
        'business.Business', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.name or self.mobile
