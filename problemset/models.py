from django.db import models
from common.consts import CheckerType, LanguageEnum


class Problem(models.Model):
    CHECKER_TYPE_CHOICES = [(t.value, t.name) for t in CheckerType]

    title = models.CharField(max_length=50)
    description = models.TextField()
    time_limit = models.IntegerField(default=2000, help_text='In ms')
    memory_limit = models.IntegerField(default=131072, help_text='In KB')
    note = models.TextField(blank=True)
    sample_inputs = models.TextField(blank=True)
    sample_outputs = models.TextField(blank=True)
    checker_type = models.SmallIntegerField(choices=CHECKER_TYPE_CHOICES)


class TestCase(models.Model):
    problem = models.OneToOneField(Problem, models.CASCADE)
    inputs = models.TextField(blank=True)
    expected_outputs = models.TextField(blank=True)


class Solution(models.Model):
    problem = models.ForeignKey(Problem, models.CASCADE)
    code = models.TextField()
    lang = models.SmallIntegerField(choices=[(t.value, t.name) for t in LanguageEnum])
    is_model_solution = models.BooleanField(default=False)
