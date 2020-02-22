from rest_framework.decorators import api_view
from django.http.response import HttpResponse, HttpResponseBadRequest
from user.models import Submission
from problemset.models import TestCase
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

    related_contest = submission.contest
    if related_contest:
        if not related_contest.is_running:
            return HttpResponse()

        standing = Standing.objects.get(contest=related_contest, user=submission.user)
        penalty = standing.penalties.get(str(submission.problem_id), 0)  # str??!!! shitty JSONField
        if penalty <= 0:
            if submission.verdict == VerdictResult.AC:
                penalty = related_contest.get_elapsed_time_to(submission.submit_time) + (-penalty) * PENALTY_FOR_ONE
            else:
                penalty -= 1
            standing.penalties[submission.problem_id] = penalty
            standing.save(update_fields=['penalties'])

            group_name = ContestStandings.GROUP_NAME_FMT.format(related_contest.id)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                group_name, {'type': 'contest.send_standings', 'contest_id': related_contest.id}
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
        test_case = TestCase.objects.get(problem_id=problem_id)
        test_case.expected_outputs = solution_res['outputs']
        test_case.save(update_fields=['expected_outputs'])

        if len(test_case.expected_outputs) != len(test_case.inputs):
            message['solution']['desc'] += "(WTF? The outputs length doesn't match the inputs length?)"

    message['type'] = 'check.send_result'
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(channel_name, message)

    return HttpResponse()
