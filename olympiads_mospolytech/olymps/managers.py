from django.db import models
from django.utils import timezone
import logging
logging.basicConfig(level=logging.INFO)


class OlympiadManager(models.Manager):
    def archive(self):
        logging.info('archive')
        return self.filter(date_finish__lt=timezone.now(), visible=True)

    def calendar(self):
        logging.info('calendar')
        return self.filter(date_finish__gt=timezone.now(), visible=True)


class LeaderboardManager(models.Manager):
    def current_score(self, user):
        return self.get(user=user).reload_score()

    def rating(self, user):
        current = self.get(user=user)

        top = self.all().filter(score__gt = current.score).order_by('-score').count()
        return 1 + top

