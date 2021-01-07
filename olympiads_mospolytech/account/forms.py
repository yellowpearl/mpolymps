from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import OlympsUser


class OlympsUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = OlympsUser
        fields = ('email',)


class OlympsUserChangeForm(UserChangeForm):
    class Meta:
        model = OlympsUser
        fields = ('email',)


class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    group = forms.CharField(max_length=16, label='Номер группы')
    phone_number = forms.CharField(max_length=16, label='Номер телефона')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторить пароль', widget=forms.PasswordInput)


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def save(self):
        user = OlympsUser.objects.create_user(self.cleaned_data['email'],
                                              self.cleaned_data['group'],
                                              self.cleaned_data['phone_number'],
                                              self.cleaned_data['password'],)
        return user