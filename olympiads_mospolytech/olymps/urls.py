from django.urls import path
from .views import *

urlpatterns = [
    path('oll/', AccountView.as_view()),
]