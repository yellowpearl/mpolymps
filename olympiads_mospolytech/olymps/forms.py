from django import forms
from .models import Olympiad, Exercise, Answer, ExtraPoints
from django.forms import modelformset_factory


class EnterEmailForm(forms.Form):
    email = forms.EmailField(label='Введите почту студента')


class AddExtraPointsForm(forms.Form):
    points = forms.IntegerField(label='Очков')

    def save(self, student):
        extra = ExtraPoints.objects.create(user=student, points=self.cleaned_data['points'])
        return extra


AnswersFormSet = modelformset_factory(Answer, fields=('points',), extra=0)
PointsFormSet = modelformset_factory(Exercise, fields=('max_points',), extra=0)


class OlympiadCreationForm(forms.Form):
    name = forms.CharField(max_length=32, label='Название')
    number_of_exercises = forms.IntegerField(label='Число заданий')
    date_start = forms.DateField(label='Начало олимпиады')
    date_finish = forms.DateField(label='Конец олимпиады')

    def save(self):
        olymp = Olympiad(
            name=self.cleaned_data['name'],
            date_start=self.cleaned_data['date_start'],
            date_finish=self.cleaned_data['date_finish'],)
        olymp.save()
        for i in range(self.cleaned_data['number_of_exercises']):
            e = Exercise(
                olympiad=olymp,
                name=i+1,
                max_points=0)
            e.save()
        return olymp
