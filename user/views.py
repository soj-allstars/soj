from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import Submission
from common.consts import VerdictResult, LanguageEnum


@api_view(['GET'])
def get_user_submission(request):
    try:
        sid = request.GET['sid']
    except KeyError:
        return Response({'info': 'Angelic Parade a.k.a. missing sid'}, status.HTTP_400_BAD_REQUEST)

    try:
        submission = Submission.objects.get(id=sid)
    except Submission.DoesNotExist:
        return Response({'info': 'invalid submission id'}, status.HTTP_400_BAD_REQUEST)

    return Response({
        'verdict': VerdictResult(submission.verdict).name,
        'memory_usage': submission.memory,
        'time_usage': submission.time,
        'submit_time': submission.submit_time,
        'code': submission.code,
        'lang': LanguageEnum(submission.lang).name,
        'outputs': submission.outputs,
    })
