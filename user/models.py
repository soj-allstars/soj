from django.db import models
from django.contrib.auth import get_user_model
from problemset.models import Problem
from common.models import Language
from common.consts import VerdictResult


class UserInfo(models.Model):
    pass


class Submission(models.Model):
    VERDICT_CHOICES = [(v.value, v.name) for v in VerdictResult]

    user = models.ForeignKey(get_user_model(), models.DO_NOTHING)
    problem = models.ForeignKey(Problem, models.DO_NOTHING)
    submit_time = models.DateTimeField()
    code = models.TextField()
    lang = models.ForeignKey(Language, models.DO_NOTHING)
    time = models.IntegerField(help_text='In ms')
    memory = models.IntegerField(help_text='In KB')
    verdict = models.SmallIntegerField(choices=VERDICT_CHOICES)
    outputs = models.TextField(help_text='a list formatted in JSON')
