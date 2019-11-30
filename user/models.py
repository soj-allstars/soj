from django.db import models
from django.contrib.auth import get_user_model
from problemset.models import Problem
from common.consts import VerdictResult, LanguageEnum


class UserInfo(models.Model):
    pass


class Submission(models.Model):
    VERDICT_CHOICES = [(v.value, v.name) for v in VerdictResult]

    user = models.ForeignKey(get_user_model(), models.DO_NOTHING)
    problem = models.ForeignKey(Problem, models.DO_NOTHING)
    submit_time = models.DateTimeField()
    code = models.TextField()
    lang = models.SmallIntegerField(choices=[(t.value, t.name) for t in LanguageEnum])
    time = models.IntegerField(help_text='In ms', null=True)
    memory = models.IntegerField(help_text='In KB', null=True)
    verdict = models.SmallIntegerField(choices=VERDICT_CHOICES, null=True)
    outputs = models.TextField(help_text='a list formatted in JSON', null=True)
    job_id = models.CharField(max_length=50, help_text='The job id in RQ', null=True)
