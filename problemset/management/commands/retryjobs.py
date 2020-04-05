from django.core.management.base import BaseCommand
from django.conf import settings
from rq.registry import FailedJobRegistry


class Command(BaseCommand):
    help = 'Retry failed judge jobs'

    def handle(self, *args, **options):
        registry = FailedJobRegistry(queue=settings.JUDGE_Q)
        for job_id in registry.get_job_ids():
            registry.requeue(job_id)
            registry.remove(job_id)
            print(f'retried job: {job_id}')
