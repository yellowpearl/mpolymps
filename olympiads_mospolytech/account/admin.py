from django.contrib import admin
from django.contrib.auth.models import User
from .models import OlympsUser, ResetPasswords, EmailConfirmation

admin.site.register(EmailConfirmation)
admin.site.register(OlympsUser)
admin.site.register(ResetPasswords)
