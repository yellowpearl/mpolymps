from django.contrib import admin
from django.contrib.auth.models import User
from .models import *

admin.site.register(EmailConfirmation)
admin.site.register(OlympsUser)
admin.site.register(ResetPasswords)
admin.site.register(Chat)
admin.site.register(Message)
