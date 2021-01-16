from django import forms
from .models import Olympiad, Exercise
from django.forms import modelformset_factory


class ExercisePoints(forms.Form):
    name = forms.CharField(label='Название')
    points = forms.IntegerField(label='Очков')

    def save(self, olympiad):
        exercise = Exercise(name=self.name, max_points=self.points, olympiad=olympiad)
        exercise.save()


PointsFormSet = modelformset_factory(Exercise, fields=('name', 'max_points'))


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
