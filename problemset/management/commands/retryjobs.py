from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from user.models import Submission
from common.consts import VerdictResult
from rq.job import Job
from rq.exceptions import InvalidJobOperation


class Command(BaseCommand):
    help = 'Retry failed judge jobs'

    def handle(self, *args, **options):
        failed_submissions = Submission.objects.filter(verdict=VerdictResult.PENDING).order_by('submit_time')
        now = timezone.now()
        for s in failed_submissions:
            if (now - s.submit_time).total_seconds() < 30:
                break

            job = Job.fetch(s.job_id, connection=settings.REDIS)
            try:
                job.requeue()
            except InvalidJobOperation:
                continue
            print(f'retried job: {s.job_id}. submission id: {s.id}. failed reason:\n{job.exc_info}')
