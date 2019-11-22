from django.db import models
from common.consts import CheckerType
from common.models import Language


class Problem(models.Model):
    CHECKER_TYPE_CHOICES = [(t.value, t.name) for t in CheckerType]

    title = models.CharField(max_length=50)
    description = models.TextField()
    time_limit = models.IntegerField(default=2000, help_text='In ms')
    memory_limit = models.IntegerField(default=131072, help_text='In KB')
    note = models.TextField()
    checker_type = models.SmallIntegerField(choices=CHECKER_TYPE_CHOICES)


class Solution(models.Model):
    problem = models.ForeignKey(Problem, models.CASCADE)
    code = models.TextField()
    language = models.ForeignKey(Language, models.DO_NOTHING)
