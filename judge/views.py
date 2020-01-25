from rest_framework.decorators import api_view
from django.http.response import HttpResponse, HttpResponseBadRequest
from user.models import Submission
import logging
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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

    return HttpResponse()


@api_view(['POST'])
def check_finished(request):
    channel_name = request.POST['channel_name']
    result = json.loads(request.POST['result'])

    solution_res = result['solution']
    checker_res = result.get('special_judge')

    message = {
        'solution_verdict': solution_res['verdict'],
        'solution_time_used': solution_res['time_usage'],
        'solution_memory_used': solution_res['memory_usage'],
        'solution_desc': str(solution_res.get('desc', ''))
    }
    if checker_res:
        message['checker_verdict'] = checker_res['verdict']
        message['checker_time_used'] = checker_res['time_usage']
        message['checker_memory_used'] = checker_res['memory_usage']
        message['checker_desc'] = str(checker_res.get('desc', ''))

    message['type'] = 'check.send_result'
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(channel_name, message)

    return HttpResponse()
