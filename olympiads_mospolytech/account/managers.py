import hashlib
from random import random

from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from olympiads_mospolytech import settings


class OlympsUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, group, phone_number, password):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('Email должен быть указан'))
        email = self.normalize_email(email)
        user = self.model(email=email, group=group, phone_number=phone_number)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class EmailConfirmationManager(models.Manager):
    def send_confirm_email(self, user):
        confirmation_key = hashlib.sha256((str(random())+user.email).encode('utf-8')).hexdigest()[:40]

        subject = _("Подтверждение регистрации на сайте олимпиад мосполитеха")
        path = reverse('extuser:confirmation', kwargs={'key': confirmation_key})
        activate_url = f'http://127.0.0.1:8000/account/confirm-email/{confirmation_key}'
        ctx = {
            'user': user,
            'activate_url': activate_url,
        }
        message = render_to_string('registration/email/confirmation_email.html', ctx)

        send_mail(subject, '', settings.EMAIL_HOST_USER, [user.email, ], html_message=message)

        return self.create(
            user=user,
            confirmation_key=confirmation_key,
            sent=timezone.now()
        )

    def confirmation(self, key):
        try:
            confirmation = self.get(confirmation_key=key)
        except self.model.DoesNotExist:
            return None
        user = confirmation.user
        if not confirmation.expire_dt():
            user.is_confirm = True
            user.is_active = True
            user.save()
        return user

