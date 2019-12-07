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
    submit_time = models.DateTimeField(auto_now_add=True)
    code = models.TextField()
    lang = models.SmallIntegerField(choices=[(t.value, t.name) for t in LanguageEnum])
    time = models.IntegerField(help_text='In ms', default=0)
    memory = models.IntegerField(help_text='In KB', default=0)
    verdict = models.SmallIntegerField(choices=VERDICT_CHOICES, null=True)
    desc = models.CharField(max_length=255, blank=True)
    outputs = models.TextField(help_text='a list formatted in JSON', null=True)
    job_id = models.CharField(max_length=50, help_text='The job id in RQ', null=True)
