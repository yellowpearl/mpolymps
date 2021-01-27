from django.urls import path
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    path('teacher/', TeacherView.as_view(), name='teacher'),
    path('teacher/add_extra_points/', EmailEnteringView.as_view(), name='extra_points'),
    path('teacher/add_extra_points/<int:student_pk>/', ExtraPointsView.as_view()),
    path('contacts/', ContactsView.as_view(), name='contacts'),

    path('olympiad/', RedirectView.as_view(url='../about/'), name='olympiad'),
    path('olympiad/create/', CreateOlympiadView.as_view()),
    path('olympiad/<int:olympiad_pk>/', OlympiadView.as_view()),
    path('olympiad/<int:olympiad_pk>/registration/', OlympiadRegistrationView.as_view(), name='olympiad_registration'),
    path('olympiad/<int:olympiad_pk>/edit_points/', EditPointsView.as_view()),
    path('olympiad/<int:olympiad_pk>/check/', EmailEnteringView.as_view()),
    path('olympiad/<int:olympiad_pk>/check/<int:student_pk>/', CheckPointsView.as_view()),


]