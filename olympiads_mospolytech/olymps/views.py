from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .models import Olympiad, check_user, registration_answers


class AccountView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, 'base.html')


class AboutView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, 'olypms/about.html')


class ContactsView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, 'olypms/contacts.html')


class CalendarView(View):
    def get(self, request, *args, **kwargs):
        ctx = {
            'olymps': Olympiad.objects.calendar()
        }
        return render(request, 'olypms/calendar.html', ctx)


class ArchiveView(View):
    def get(self, request, *args, **kwargs):
        ctx = {
            'olymps': Olympiad.objects.archive()
        }
        return render(request, 'olypms/archive.html', ctx)


class OlympiadView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect('/account/login')

        ctx = check_user(user, pk)
        return render(request, 'olypms/olymp.html', ctx)


class OlympiadRegistrationView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect('/account/login')
        if check_user(user, pk)['is_done']:
            return HttpResponseRedirect(f'../{pk}')
        registration_answers(user, pk)
        return HttpResponseRedirect(f'../{pk}')


class TeacherView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_authenticated and user.is_teacher):
            return HttpResponseRedirect('/account/profile')

        return render(request, 'olypms/teacher.html')