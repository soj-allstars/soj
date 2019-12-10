from django_mysql.models import Model
from django.db import models
from common.consts import CheckerType, LanguageEnum
from django_mysql.models.fields import JSONField


class Problem(Model):
    CHECKER_TYPE_CHOICES = [(t.value, t.name) for t in CheckerType]

    title = models.CharField(max_length=50)
    description = models.TextField()
    time_limit = models.IntegerField(default=2000, help_text='In ms')
    memory_limit = models.IntegerField(default=131072, help_text='In KB')
    note = models.TextField(blank=True)
    sample_inputs = JSONField(default=list)
    sample_outputs = JSONField(default=list)
    checker_type = models.SmallIntegerField(choices=CHECKER_TYPE_CHOICES)

    def __str__(self):
        return self.title


class TestCase(Model):
    problem = models.OneToOneField(Problem, models.CASCADE)
    inputs = JSONField(default=list)
    expected_outputs = JSONField(default=list)


class Solution(Model):
    problem = models.ForeignKey(Problem, models.CASCADE)
    code = models.TextField()
    lang = models.SmallIntegerField(choices=[(t.value, t.name) for t in LanguageEnum])
    is_model_solution = models.BooleanField(default=False)
