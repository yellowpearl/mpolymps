from django.contrib import admin
from .models import Olympiad, Leaderboard, Exercise, Answer, ExtraPoints

admin.site.register(Olympiad)
admin.site.register(Leaderboard)
admin.site.register(Exercise)
admin.site.register(Answer)
admin.site.register(ExtraPoints)
