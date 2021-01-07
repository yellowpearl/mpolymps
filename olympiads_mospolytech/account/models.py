from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import OlympsUserManager


class NotVerifyEmails(models.Model):
    email = models.ForeignKey('OlympsUser', on_delete=models.CASCADE)
    hash = models.CharField(max_length=130)

    def __str__(self):
        return self.email


class ResetPasswords(models.Model):
    email = models.ForeignKey('OlympsUser', on_delete=models.CASCADE)
    hash = models.CharField(max_length=130)

    def __str__(self):
        return self.email


class OlympsUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_mail_confirmed = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    group = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = OlympsUserManager()

    def __str__(self):
        return self.email
