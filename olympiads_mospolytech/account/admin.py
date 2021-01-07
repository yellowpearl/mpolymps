from django.contrib import admin
from django.contrib.auth.models import User
from .models import NotVerifyEmails, OlympsUser, ResetPasswords

admin.site.register(NotVerifyEmails)
admin.site.register(User, OlympsUser)
admin.site.register(ResetPasswords)
