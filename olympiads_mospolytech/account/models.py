import datetime
from olympiads_mospolytech.settings import EMAIL_CONFIRMATION_DAYS
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import OlympsUserManager, EmailConfirmationManager
from ..olymps.models import Olympiad


class ResetPasswords(models.Model):
    email = models.ForeignKey('OlympsUser', on_delete=models.CASCADE)
    hash = models.CharField(max_length=130)

    def __str__(self):
        return self.email


class OlympsUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=30, default='unknown')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_mail_confirmed = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    group = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    date_joined = models.DateTimeField(default=timezone.now)
    olympiads = models.ManyToManyField(Olympiad)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = OlympsUserManager()

    def save(self, *args, **kwargs):
        super(OlympsUser, self).save(*args, **kwargs)
        if not self.is_active:
            EmailConfirmation.objects.send_confirm_email(self)

    def __str__(self):
        return self.email


class EmailConfirmation(models.Model):
    user = models.OneToOneField(OlympsUser, on_delete=models.CASCADE)
    confirmation_key = models.CharField(max_length=40)
    sent = models.DateTimeField()

    objects = EmailConfirmationManager()

    def __str__(self):
        return f'For {str(self.user)}'

    def expire_dt(self):
        expired = self.sent + datetime.timedelta(days=EMAIL_CONFIRMATION_DAYS)
        return timezone.now() >= expired
