from django.conf import settings
from problemset.models import Solution
from common.consts import LanguageEnum, CheckerType
import logging


def send_judge_request(problem, submission):
    solution = Solution.objects.get(problem=problem, is_model_solution=True)  # catch exception outside

    judge_job = settings.JUDGE_Q.enqueue(
        'job_dealer.judge_submission',
        submit_id=submission.id,
        problem_id=problem.id,
        submitted_code=submission.code,
        submitted_lang=LanguageEnum(submission.lang).name,
        time_limit=problem.time_limit,
        memory_limit=problem.memory_limit,
        solution_code=solution.code,
        solution_lang=LanguageEnum(solution.lang).name,
        checker_type=CheckerType(problem.checker_type).name,
    )
    submission.job_id = judge_job.id
    submission.save()
