from django.db import models
from django.shortcuts import get_object_or_404
import logging
from .managers import LeaderboardManager, OlympiadManager
logging.basicConfig(level=logging.INFO)


class ResponseExercise:
    def __init__(self, name, points, max_points):
        self.name = name
        self.points = points
        self.max_points = max_points


def check_user(user, olympiad):
    exercises = Exercise.objects.filter(olympiad=olympiad)
    resps = []
    for exercise in exercises:
        try:
            answer = Answer.objects.get(exercise=exercise, user=user)
            resp = ResponseExercise(exercise.name, answer.points, exercise.max_points)
            resps.append(resp)

        except:
            return {
                'is_done': False,
                'olympiad': olympiad,
            }
    checked = OlympiadIsChecked.objects.get(olympiad=olympiad, user=user)
    return {
        'is_done': True,
        'is_checked': checked.is_checked,
        'olympiad': olympiad,
        'resps': resps,
    }


def registration_answers(user, olympiad_pk):
    olympiad = Olympiad.objects.get(pk=olympiad_pk)
    exercises = Exercise.objects.filter(olympiad=olympiad)
    for exercise in exercises:
        Answer.objects.create(user=user, exercise=exercise, points=0)
    user.olympiads.add(olympiad)
    OlympiadIsChecked.objects.create(user=user, olympiad=olympiad)

class ExtraPoints(models.Model):
    user = models.ForeignKey('account.OlympsUser', on_delete=models.CASCADE)
    points = models.IntegerField(default=0)


class Answer(models.Model):
    exercise = models.ForeignKey('Exercise', default=1, on_delete=models.CASCADE)
    user = models.ForeignKey('account.OlympsUser', on_delete=models.CASCADE)
    points = models.IntegerField(default=0)


class Exercise(models.Model):
    olympiad = models.ForeignKey('Olympiad', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    max_points = models.IntegerField()

    def __str__(self):
        return str(self.olympiad) + ' ' + self.name


class Olympiad(models.Model):
    name = models.CharField(max_length=128)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    visible = models.BooleanField(default=True)

    objects = OlympiadManager()
    def __str__(self):
        return self.name


class Leaderboard(models.Model):
    user = models.ForeignKey('account.OlympsUser', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    objects = LeaderboardManager()

    def reload_score(self):
        answers = Answer.objects.filter(user=self.user).aggregate(models.Sum("points"))
        others = ExtraPoints.objects.filter(user=self.user).aggregate(models.Sum("points"))
        self.score = answers['points__sum'] + others['points__sum']
        self.save()
        return self.score


class OlympiadIsChecked(models.Model):
    user = models.ForeignKey('account.OlympsUser', on_delete=models.CASCADE)
    olympiad = models.ForeignKey('Olympiad', on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)
