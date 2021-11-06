from rest_framework.decorators import api_view
from django.http.response import HttpResponse, HttpResponseBadRequest
from user.models import Submission
from problemset.models import Problem
from problemset.consumers import SubmissionInfo
import logging
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from common.consts import VerdictResult, PENALTY_FOR_ONE
from contest.models import Standing
from contest.consumers import ContestStandings


@api_view(['POST'])
def judge_finished(request):
    submit_id = request.POST['submit_id']
    result = json.loads(request.POST['result'])

    try:
        submission = Submission.objects.get(id=submit_id)
    except Submission.DoesNotExist:
        logging.warning(f'[judge_finished] submission does not exist. {submit_id=}')
        return HttpResponseBadRequest()

    submission.verdict = result['verdict']
    submission.desc = str(result.get('desc', ''))
    submission.time = result['time_usage']
    submission.memory = result['memory_usage']
    submission.outputs = result['outputs']
    submission.save()

    basic_info = SubmissionInfo.get_submission_info(submission)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(  # detail
        SubmissionInfo.DETAIL_GROUP_NAME_FMT.format(submission_id=submit_id),
        {
            'type': 'submission.send_info',
            **basic_info,
        }
    )

    related_contest = submission.contest
    if related_contest:
        standing, _ = Standing.objects.get_or_create(contest=related_contest, user=submission.user)
        str_problem_id = str(submission.problem_id)  # because JSON field name must be str.

        AC_time = standing.AC_times.get(str_problem_id)
        wrong_number = standing.wrong_numbers.get(str_problem_id, 0)
        if AC_time is None:  # only update standing info when not AC or the on the very first AC
            if submission.verdict == VerdictResult.AC:
                AC_time = related_contest.get_elapsed_time_to(submission.submit_time)
                penalty = AC_time + wrong_number * PENALTY_FOR_ONE

                standing.AC_times[str_problem_id] = AC_time
                standing.total_penalty += penalty
            else:
                wrong_number += 1
                standing.wrong_numbers[str_problem_id] = wrong_number
            standing.save()

            group_name = ContestStandings.GROUP_NAME_FMT.format(related_contest.id)
            async_to_sync(channel_layer.group_send)(
                group_name, {'type': 'contest.send_standings', 'contest_id': related_contest.id}
            )

        async_to_sync(channel_layer.group_send)(  # contest
            SubmissionInfo.CONTEST_LIST_GROUP_NAME_FMT.format(
                contest_id=related_contest.id
            ),
            {'type': 'submission.send_info', **basic_info}
        )
    else:  # only not contest submission sends to `user` and `all`
        async_to_sync(channel_layer.group_send)(  # user
            SubmissionInfo.USER_LIST_GROUP_NAME_FMT.format(user_id=submission.user_id),
            {'type': 'submission.send_info', **basic_info}
        )
        async_to_sync(channel_layer.group_send)(  # all
            SubmissionInfo.ALL_LIST_GROUP_NAME_FMT,
            {'type': 'submission.send_info', **basic_info}
        )

    return HttpResponse()


@api_view(['POST'])
def check_finished(request):
    problem_id = request.POST['problem_id']
    channel_name = request.POST['channel_name']
    result = json.loads(request.POST['result'])

    solution_res = result['solution']
    checker_res = result.get('special_judge')

    message = {}
    message['solution'] = {
        'verdict': VerdictResult(solution_res['verdict']).name,
        'time_used': solution_res['time_usage'],
        'memory_used': solution_res['memory_usage'],
        'desc': str(solution_res.get('desc', ''))
    }
    if checker_res:
        message['checker'] = {
            'verdict': VerdictResult(checker_res['verdict']).name,
            'time_used': checker_res['time_usage'],
            'memory_used': checker_res['memory_usage'],
            'desc': str(checker_res.get('desc', ''))
        }

    if solution_res['verdict'] == VerdictResult.AC:
        outputs = solution_res['outputs']
        problem = Problem.objects.only('sample_inputs').get(id=problem_id)
        problem.sample_outputs = outputs[:len(problem.sample_inputs)]
        problem.save(update_fields=['sample_outputs'])

    if channel_name:
        message['type'] = 'check.send_result'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(channel_name, message)

    return HttpResponse()
