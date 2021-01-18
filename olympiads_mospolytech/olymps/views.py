from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .models import Olympiad, check_user, registration_answers
from ..account.models import OlympsUser
from .forms import *

import logging
logging.basicConfig(level=logging.INFO)


class BaseOlympiadView(View):
    def is_teacher(self, user):
        if user.is_authenticated and user.is_teacher:
            return True
        else:
            return False

    def is_authenticated(self, user):
        if user.is_authenticated:
            return True
        else:
            return False


class AccountView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'olymps/about.html')


class ContactsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'olymps/contacts.html')


class CalendarView(View):
    def get(self, request, *args, **kwargs):
        ctx = {
            'olymps': Olympiad.objects.calendar()
        }
        return render(request, 'olymps/calendar.html', ctx)


class ArchiveView(View):
    def get(self, request, *args, **kwargs):
        ctx = {
            'olymps': Olympiad.objects.archive()
        }
        return render(request, 'olymps/archive.html', ctx)


class OlympiadView(BaseOlympiadView):
    def get(self, request, *args, **kwargs):
        pk = kwargs['olympiad_pk']
        user = request.user
        if not self.is_authenticated(user):
            return HttpResponseRedirect('/account/login')

        ctx = check_user(user, pk)
        return render(request, 'olymps/olymp.html', ctx)


class OlympiadRegistrationView(BaseOlympiadView):
    def get(self, request, *args, **kwargs):
        pk = kwargs['olympiad_pk']
        user = request.user
        if not self.is_authenticated(user):
            return HttpResponseRedirect('/account/login')
        if check_user(user, pk)['is_done']:
            return HttpResponseRedirect(f'../')
        registration_answers(user, pk)
        return HttpResponseRedirect(f'../')


class TeacherView(BaseOlympiadView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not self.is_teacher(user):
            return HttpResponseRedirect('/account/profile')

        return render(request, 'olymps/teacher.html')


class AddExtraPointsView(BaseOlympiadView):
    def get(self, request, **kwargs):
        user = request.user
        if not self.is_teacher(user):
            return HttpResponseRedirect('/account/profile')
        form = AddExtraPointsForm()
        return render(request, 'olymps/add_extra_points.html', {'form': form})

    def post(self, request, **kwargs):
        user = request.user
        if not self.is_teacher(user):
            return HttpResponseRedirect('/account/profile')
        student_pk = kwargs['student_pk']
        student = OlympsUser.objects.get(pk=student_pk)
        form = AddExtraPointsForm(request.POST)
        if form.is_valid():
            extra = form.save(student)
            return HttpResponseRedirect('/teacher')


class CreateOlympiadView(BaseOlympiadView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not self.is_teacher(user):
            return HttpResponseRedirect('/account/profile')
        form = OlympiadCreationForm()
        return render(request, 'olymps/create_olympiad.html', {'form': form})

    def post(self, request):
        user = request.user
        if not self.is_teacher(user):
            return HttpResponseRedirect('/account/profile')
        form = OlympiadCreationForm(request.POST)
        if form.is_valid():
            olymp = form.save()
            return HttpResponseRedirect(f'../{olymp.pk}/edit_points')


class EditPointsView(BaseOlympiadView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not self.is_teacher(user):
            return HttpResponseRedirect('/account/profile')

        pk = kwargs['olympiad_pk']
        olympiad = Olympiad.objects.get(pk=pk)
        form = PointsFormSet(queryset=Exercise.objects.filter(olympiad=olympiad))
        return render(request, 'olymps/edit_points.html', {'form': form})

    def post(self, request, **kwargs):
        user = request.user
        if not self.is_teacher(user):
            return HttpResponseRedirect('/account/profile')

        pk = kwargs['olympiad_pk']
        olympiad = Olympiad.objects.get(pk=pk)
        form = PointsFormSet(request.POST)
        for f in form:
            f.olympiad = olympiad
        if form.is_valid():
            exercises = form.save()
            return HttpResponseRedirect(f'../')
        else:
            return HttpResponse(f'{form.errors}')


class CheckOlympiadView(BaseOlympiadView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not self.is_teacher(user):
            return HttpResponseRedirect('/account/profile')
        form = CheckEmailForm()
        return render(request, 'olymps/edit_points.html', {'form': form})

    def post(self, request, **kwargs):
        user = request.user
        if not self.is_teacher(user):
            return HttpResponseRedirect('/account/profile')
        form = CheckEmailForm(request.POST)
        if form.is_valid():
            student = OlympsUser.objects.get(email=form.cleaned_data['email'])
            return HttpResponseRedirect(f'./{student.pk}')


class CheckPointsView(BaseOlympiadView):
    def get(self, request, *args, **kwargs):
        user = request.user
        student_pk = kwargs['student_pk']
        if not self.is_teacher(user):
            return HttpResponseRedirect('/account/profile')
        pk = kwargs['olympiad_pk']

        olympiad = Olympiad.objects.get(pk=pk)
        student = OlympsUser.objects.get(pk=student_pk)
        exercises = Exercise.objects.filter(olympiad=olympiad)
        form = AnswersFormSet(queryset=Answer.objects.filter(user=student, exercise__in=exercises))
        return render(request, 'olymps/edit_points.html', {'form': form})

    def post(self, request, **kwargs):
        user = request.user
        student_pk = kwargs['student_pk']
        student = OlympsUser.objects.get(pk=student_pk)
        if not self.is_teacher(user):
            return HttpResponseRedirect('/account/profile')

        pk = kwargs['olympiad_pk']
        olympiad = Olympiad.objects.get(pk=pk)
        form = AnswersFormSet(request.POST)
        for f in form:
            f.user = user
        if form.is_valid():
            answers = form.save()
            return HttpResponseRedirect(f'/olympiad/{pk}')
        else:
            return HttpResponse(f'{form.errors}')
