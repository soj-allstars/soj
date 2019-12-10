from django.db import models
from django_mysql.models import Model
from django.contrib.auth import get_user_model
from problemset.models import Problem


class Contest(Model):
    name = models.CharField(max_length=255)
    problems = models.ManyToManyField(Problem)
    Announcement = models.TextField(blank=True)
    users = models.ManyToManyField(get_user_model())
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name
