from django.db import models
from django.contrib.auth import get_user_model
from problemset.models import Problem


class Contest(models.Model):
    name = models.CharField(max_length=255)
    problems = models.ManyToManyField(Problem)
    Announcement = models.TextField()
    users = models.ManyToManyField(get_user_model())
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
