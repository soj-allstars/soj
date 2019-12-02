from rest_framework.decorators import api_view
from django.http.response import HttpResponse, HttpResponseBadRequest
from user.models import Submission
import json
import logging


@api_view(['POST'])
def judge_finished(request):
    result = request.POST.get('result')

    sub_id = result['sub_id']
    try:
        submission = Submission.objects.get(id=sub_id)
    except Submission.DoesNotExist:
        logging.info(f'[judge_finished] submission does not exist. {sub_id=}')
        return HttpResponseBadRequest()

    submission.verdict = result['verdict']
    submission.desc = result.get('desc', '')
    submission.time = result['time_usage']
    submission.memory = result['memory_usage']
    submission.outputs = json.dumps(result['outputs'])
    submission.save()

    return HttpResponse()
