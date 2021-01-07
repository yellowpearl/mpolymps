from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .forms import UserRegistrationForm
from .models import OlympsUser, EmailConfirmation


class AccountView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')

    def post(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')


class SignUp(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('http://127.0.0.1:8000/account/login')


def confirmation_email(request, key):
    user = EmailConfirmation.objects.confirmation(key.lower())
    if user:
        if user.is_confirm:
            activate = "Активация прошла успешно"
        else:
            activate = "Период активации истек"
        return render(request, 'confirm_email_done.html', context=activate)
    activate = "Период активации истек"
    return render(request, 'confirm_email_done.html', context=activate)