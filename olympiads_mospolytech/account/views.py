from django.db.models import Prefetch, Q
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, redirect
from django.views.generic import View
from .forms import *
from .models import OlympsUser, EmailConfirmation
from ..olymps.models import Leaderboard, Olympiad
from ..olymps.managers import LeaderboardManager
from django.contrib.auth import views as auth_views
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
            'position': Leaderboard.objects.rating(user),
            'messages': Message.objects.get_last_messages_by_user(user, Chat)
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


class OlympLoginView(auth_views.LoginView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return HttpResponseRedirect('/account/profile')
        else:
            return self.render_to_response(self.get_context_data())


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


class NewChatView(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect('../login')
        form = NewChatForm()
        return render(request, 'registration/new_chat.html', {'form': form})

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect('../login')
        form = NewChatForm(request.POST)
        if form.is_valid():
            user_to = form.save(user)
            return HttpResponseRedirect(f'../chat/{user_to.pk}')
        else:
            return render(request, 'registration/new_chat.html', {'form': form})


class ChatView(View):
    def get(self, request, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect('../login')
        logging.info('before')
        user_to = get_object_or_404(OlympsUser, pk=kwargs['user_pk'])
        chat = Chat.objects.get_by_users(user, user_to)
        if chat is None:
            return HttpResponseRedirect('../new-chat')
        messages = Message.objects.filter(chat=chat).order_by('-create_time')
        not_checked = Message.objects.filter(chat=chat, is_checked=False, msg_to=user)
        for msg in not_checked:
            msg.is_checked = True
            msg.save()
        form = NewMessageForm()
        return render(request, 'registration/chat.html', {'form': form, 'messages': messages})

    def post(self, request, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect('../login')
        user_to = get_object_or_404(OlympsUser, pk=kwargs['user_pk'])
        chat = Chat.objects.get_by_users(user, user_to)
        logging.info('before')
        if chat is None:
            logging.info('none')
            return HttpResponseRedirect(f'/new-chat')
        logging.info('not none')
        form = NewMessageForm(request.POST)
        if form.is_valid():
            logging.info('valid')
            msg = form.save(user, user_to, chat)
        logging.info('post valid')
        return redirect(request.META['HTTP_REFERER'])
