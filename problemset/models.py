from django.db import models
from common.consts import CheckerType


class Problem(models.Model):
    CHECKER_TYPE_CHOICES = [(t.value, t.name) for t in CheckerType]

    title = models.CharField(max_length=50)
    description = models.TextField()
    time_limit = models.IntegerField(default=2000, help_text='In ms')
    memory_limit = models.IntegerField(default=128, help_text='In MB')
    note = models.TextField()
    checker_type = models.SmallIntegerField(choices=CHECKER_TYPE_CHOICES)
