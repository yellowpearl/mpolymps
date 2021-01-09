from django.urls import path
from .views import *

urlpatterns = [
    path('about/', AccountView.as_view(), name='about'),
    path('calendar/', AccountView.as_view(), name='calendar'),
    path('archive/', AccountView.as_view(), name='archive'),
    path('contact/', AccountView.as_view(), name='contact'),
]