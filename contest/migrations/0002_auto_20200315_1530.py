# Generated by Django 2.2.9 on 2020-03-15 07:30

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standing',
            name='penalties',
        ),
        migrations.AddField(
            model_name='standing',
            name='AC_times',
            field=django_mysql.models.JSONField(blank=True, default=dict, help_text='problem_id:AC_time(unit: s) mapping'),
        ),
        migrations.AddField(
            model_name='standing',
            name='total_penalty',
            field=models.FloatField(default=0, help_text='unit: s'),
        ),
        migrations.AddField(
            model_name='standing',
            name='wrong_numbers',
            field=django_mysql.models.JSONField(blank=True, default=dict, help_text='problem_id:wrong_submission_number mapping'),
        ),
    ]
