from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .forms import UserRegistrationForm
from .models import OlympsUser, EmailConfirmation
from ..olymps.models import Leaderboard, Olympiad
from ..olymps.managers import LeaderboardManager
import logging
logging.basicConfig(level=logging.INFO)

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect('../login')
        ctx = {
            'user': user,
            'olympiads': user.olympiads.filter(visible=True),
            'score': Leaderboard.objects.current_score(user),
            'position': Leaderboard.objects.rating(user)
        }
        return render(request, 'registration/profile.html', ctx)


class SignUp(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return HttpResponseRedirect('../profile')
        form = UserRegistrationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            return HttpResponseRedirect('../profile')
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('../login')


def confirmation_email(request, **kwargs):
    key = kwargs['key']
    user = EmailConfirmation.objects.confirmation(key.lower())
    if user:
        if user.is_mail_confirmed:
            activate = "Активация прошла успешно"
        else:
            activate = "Период активации истек"
        return render(request, 'registration/confirm_email_done.html', {'activate': activate}, )
    activate = "Период активации истек"
    return render(request, 'registration/confirm_email_done.html', {'activate': activate}, )
