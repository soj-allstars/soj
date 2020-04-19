from django.db import models
from django_mysql.models import Model, JSONField
from django.contrib.auth import get_user_model
from problemset.models import Problem
from django.utils import timezone
from common.consts import ContestCategory


class Contest(Model):
    CATEGORY_CHOICES = [(t.value, t.name) for t in ContestCategory]

    name = models.CharField(max_length=255)
    problems = models.ManyToManyField(Problem, through='ContestProblem', blank=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(get_user_model(), blank=True, help_text='registered users or entered-password users')
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField()
    visible = models.BooleanField(default=False, db_index=True)
    category = models.SmallIntegerField(choices=CATEGORY_CHOICES, default=ContestCategory.OPEN)
    password = models.CharField(max_length=50, null=True, blank=True, help_text='only used if category is PRIVATE')

    def is_user_registered(self, user):
        return (
            user.is_authenticated and
            user.contest_set.filter(id=self.id).exists()
        )

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


class ContestProblem(Model):
    contest = models.ForeignKey(Contest, models.CASCADE)
    problem = models.ForeignKey(Problem, models.CASCADE)
    problem_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('problem_order',)


class Standing(Model):
    contest = models.ForeignKey(Contest, models.CASCADE)
    AC_times = JSONField(blank=True, help_text="problem_id:AC_time(unit: s) mapping")
    wrong_numbers = JSONField(blank=True, help_text="problem_id:wrong_submission_number mapping")
    total_penalty = models.FloatField(default=0, help_text="unit: s")
    user = models.ForeignKey(get_user_model(), models.DO_NOTHING)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['contest', 'user'], name='unique_contest_user'),
        ]

    @property
    def real_AC_times(self):
        """:return problem_no:AC_time mapping"""
        AC_times = {}
        for problem_id, time in self.AC_times.items():
            order = ContestProblem.objects.get(contest=self.contest, problem_id=problem_id).problem_order
            AC_times[chr(ord('A') + order - 1)] = time

        return AC_times

    @property
    def real_wrong_numbers(self):
        """:return problem_no:wrong_number mapping"""
        wrong_numbers = {}
        for problem_id, number in self.wrong_numbers.items():
            order = ContestProblem.objects.get(contest=self.contest, problem_id=problem_id).problem_order
            wrong_numbers[chr(ord('A') + order - 1)] = number

        return wrong_numbers
