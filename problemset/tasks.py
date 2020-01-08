from django.conf import settings


def send_check_request(detail):
    check_job = settings.JUDGE_Q.enqueue(
        'judge_jobs.check_solution_and_checker', **detail
    )
    return check_job.id
