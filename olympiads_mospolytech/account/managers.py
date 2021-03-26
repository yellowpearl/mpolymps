import hashlib
from random import random
import logging
logging.basicConfig(level=logging.INFO)

from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.db.models import Prefetch, Q
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from olympiads_mospolytech import settings
from ..olymps.models import Leaderboard, Answer, ExtraPoints


class OlympsUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, name, group, phone_number, password, *args, **kwargs):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('Email должен быть указан'))
        email = self.normalize_email(email)
        user = self.model(email=email, group=group, phone_number=phone_number, name=name)
        user.set_password(password)
        user.save()
        Leaderboard.objects.create(user=user)
        Answer.objects.create(user=user)
        ExtraPoints.objects.create(user=user)
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
        logging.info('conf')
        try:
            logging.info('try')
            confirmation = self.get(confirmation_key=key)
        except self.model.DoesNotExist:
            return None
        user = confirmation.user
        logging.info('weq')
        if not confirmation.expire_dt():
            user.is_mail_confirmed = True
            user.is_active = True
            user.save()
        return user


class ChatManager(BaseUserManager):
    def get_by_users(self, user1, user2):
        try:
            chat = self.get(user1=user1, user2=user2)
            return chat
        except:
            try:
                chat = self.get(user1=user2, user2=user1)
                return chat
            except:
                return None


class MessageManager(models.Manager):
    def get_last_messages_by_user(self, user, chat):
        """
        chats = chat.objects.filter(Q(user1=user) | Q(user2=user))
        return [self.filter(chat=c).latest('create_time') for c in chats]
        """
        chat_list = []
        resp_messages = []
        messages = self.filter(msg_to=user).order_by('-create_time').select_related('chat')
        for m in messages:
            if m.chat not in chat_list:
                chat_list.append(m.chat)
                resp_messages.append(m)
        return resp_messages

# aa