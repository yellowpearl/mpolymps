from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    path('login/', OlympLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('signup/', SignUp.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('new-chat/', NewChatView.as_view(), name='new_chat'),
    path('chat/', RedirectView.as_view(url='../new-chat/'), name='chat'),
    path('chat/<user_pk>', ChatView.as_view()),

    path('confirm-email/<key>', confirmation_email, name="confirm"),

    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
