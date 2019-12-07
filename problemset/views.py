from common.consts import LanguageEnum
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from problemset.models import Problem
from user.models import Submission
import logging


class QuestionDetail(TemplateView):
    template_name = 'index.html'


@api_view(['GET'])
def get_problem_detail(request):
    try:
        problem_id = request.GET['pid']
    except KeyError:
        return Response({'info': 'Kawaii make MY day! a.k.a. missing pid'}, status.HTTP_400_BAD_REQUEST)

    try:
        problem = Problem.objects.get(id=problem_id)
    except Problem.DoesNotExist:
        return Response({'info': 'Invalid problem id'}, status.HTTP_400_BAD_REQUEST)
    return Response({
        'title': problem.title,
        'time_limit': problem.time_limit,
        'memory_limit': problem.memory_limit,
        'description': problem.description,
        'sample_inputs': problem.sample_inputs,
        'sample_outputs': problem.sample_outputs,
        'note': problem.note,
    })


@api_view(['POST'])
def do_submission(request):
    try:
        problem_id = request.POST['pid']
        code = request.POST['code']
        lang = request.POST['lang']
    except KeyError:
        return Response({'info': 'God Bless You a.k.a. missing parameter(s)'}, status.HTTP_400_BAD_REQUEST)

    try:
        submission = Submission()
        submission.user = request.user
        submission.problem_id = problem_id
        submission.code = code
        submission.lang = getattr(LanguageEnum, lang).value
        submission.save()
    except Exception as exception:
        logging.error(f'[do_submission] {exception=}')
        return Response({'info': 'something went wrong, please contact yjp.'},
                        status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response()
