from django.db import models
from django_mysql.models import Model, JSONField
from django.contrib.auth import get_user_model
from problemset.models import Problem
from django.utils import timezone
from common.consts import ContestCategory


class Contest(Model):
    CATEGORY_CHOICES = [(t.value, t.name) for t in ContestCategory]

    name = models.CharField(max_length=255)
    problems = models.ManyToManyField(Problem, blank=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(get_user_model(), blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    visible = models.BooleanField(default=False)
    category = models.SmallIntegerField(choices=CATEGORY_CHOICES, default=ContestCategory.OPEN)
    password = models.CharField(max_length=50, null=True, blank=True)

    @property
    def is_started(self):
        return timezone.now() >= self.start_time

    @property
    def is_running(self):
        return self.start_time <= timezone.now() <= self.end_time

    def get_elapsed_time_to(self, this_time):
        """get elapsed time from the beginning of the contest to this_time
        :return In second.
        """
        return (this_time - self.start_time).total_seconds()

    def __str__(self):
        return self.name


class Standing(Model):
    contest = models.ForeignKey(Contest, models.CASCADE)
    penalties = JSONField(blank=True, help_text="problem_id:penalty mapping, if penalty is negative, "
                                                "it represents the number of wrong submissions")
    user = models.ForeignKey(get_user_model(), models.DO_NOTHING)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['contest', 'user'], name='unique_contest_user'),
        ]
