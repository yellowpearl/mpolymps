from django.urls import path
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    path('teacher/', TeacherView.as_view(), name='teacher'),
    path('contacts/', ContactsView.as_view(), name='contacts'),

    path('olympiad/', RedirectView.as_view(url='../about/'), name='olympiad'),
    path('olympiad/<int:pk>', OlympiadView.as_view()),
    path('olympiad/<int:pk>/check', CheckOlympiadView.as_view()),
    path('olympiad/<int:olympiad_pk>/check/<int:user_pk>', CheckOlympiadView.as_view()),
    path('olympiad/registration/<int:pk>', OlympiadRegistrationView.as_view(), name='olympiad_registration'),
    path('olympiad/create/', CreateOlympiadView.as_view()),
    path('olympiad/<int:pk>/edit_points', EditPointsView.as_view()),


]