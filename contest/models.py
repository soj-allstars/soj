from django.db import models
from django_mysql.models import Model
from django.contrib.auth import get_user_model
from problemset.models import Problem
from django.utils import timezone


class Contest(Model):
    name = models.CharField(max_length=255)
    problems = models.ManyToManyField(Problem, blank=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(get_user_model(), blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    visible = models.BooleanField(default=False)

    @property
    def is_running(self):
        return self.start_time <= timezone.now() <= self.end_time

    def __str__(self):
        return self.name
