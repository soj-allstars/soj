from django.conf import settings
from problemset.models import Solution
from common.consts import LanguageEnum, CheckerType


def send_judge_request(problem, submission):
    solution = Solution.objects.get(problem=problem, is_model_solution=True)  # catch exception outside

    judge_job = settings.JUDGE_Q.enqueue(
        'judge_jobs.judge_submission',
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


def send_check_request(problem, channel_name=None):
    solution = Solution.objects.get(problem=problem, is_model_solution=True)  # catch exception outside

    check_job = settings.CHECK_Q.enqueue(
        'judge_jobs.check_solution_and_checker',
        channel_name=channel_name,
        problem_id=problem.id,
        solution_code=solution.code,
        solution_lang=LanguageEnum(solution.lang).name,
        time_limit=problem.time_limit,
        memory_limit=problem.memory_limit,
        sj_code=problem.checker_code if problem.checker_type == CheckerType.special_judge else None,
        sj_name=f'sj_{problem.id}' if problem.checker_type == CheckerType.special_judge else None,
    )
    return check_job.id
