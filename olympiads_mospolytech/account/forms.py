from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import OlympsUser, Chat, Message
from django.utils import timezone
import logging
logging.basicConfig(level=logging.INFO)


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label='Адрес электронной почты')
    name = forms.CharField(max_length=32, label='ФИО')
    group = forms.CharField(max_length=16, label='Номер группы')
    phone_number = forms.CharField(max_length=32, label='Номер телефона')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторить пароль', widget=forms.PasswordInput)


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def save(self):
        user = OlympsUser.objects.create_user(self.cleaned_data['email'],
                                              self.cleaned_data['name'],
                                              self.cleaned_data['group'],
                                              self.cleaned_data['phone_number'],
                                              self.cleaned_data['password'],)
        return user


class NewChatForm(forms.Form):
    email_to = forms.EmailField(label='Адрес электронной почты')
    text = forms.CharField(max_length=300, label='Введите сообщение')

    def clean_email_to(self):
        try:
            return OlympsUser.objects.get(email=self.cleaned_data['email_to'])
        except:
            raise forms.ValidationError('Данного пользователя не существует')

    def save(self, user):
        user_to = self.cleaned_data['email_to']
        chat_exist = Chat.objects.get_by_users(user, user_to)
        if chat_exist is None:
            chat_exist = Chat(user1=user, user2=user_to)
            chat_exist.save()
        msg = Message(msg_from=user,
                      msg_to=user_to,
                      chat=chat_exist,
                      text=self.cleaned_data['text'],
                      create_time=timezone.now())
        msg.save()
        return user_to


class NewMessageForm(forms.Form):
    text = forms.CharField(max_length=300, label='Введите сообщение')

    def save(self, user_from, user_to, chat):
        msg = Message(msg_from=user_from,
                      msg_to=user_to,
                      chat=chat,
                      text=self.cleaned_data['text'],
                      create_time=timezone.now())
        msg.save()
        return msg
