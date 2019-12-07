from common.consts import LanguageEnum, VerdictResult
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from problemset.models import Problem
from user.models import Submission
import logging


class ProblemView(APIView):
    def get(self, request):
        problem_id = request.GET['pid']

        problem = Problem.objects.get(id=problem_id)

        return Response({
            'title': problem.title,
            'time_limit': problem.time_limit,
            'memory_limit': problem.memory_limit,
            'description': problem.description,
            'sample_inputs': problem.sample_inputs,
            'sample_outputs': problem.sample_outputs,
            'note': problem.note,
        })

    def post(self, request):
        raise NotImplementedError

    def delete(self, request):
        problem_id = request.GET['pid']

        problem = Problem.objects.get(id=problem_id)

        problem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubmissionView(APIView):
    def get(self, request):
        sid = request.GET['sid']

        submission = Submission.objects.get(id=sid)

        return Response({
            'verdict': VerdictResult(submission.verdict).name if submission.verdict is not None else 'PENDING',
            'memory_usage': submission.memory,
            'time_usage': submission.time,
            'submit_time': submission.submit_time,
            'code': submission.code,
            'lang': LanguageEnum(submission.lang).name,
            'outputs': submission.outputs,
        })

    def post(self, request):
        problem_id = request.POST['pid']
        code = request.POST['code']
        lang = request.POST['lang']

        try:
            submission = Submission()
            submission.user = request.user
            submission.problem_id = problem_id
            submission.code = code
            submission.lang = getattr(LanguageEnum, lang).value
            submission.save()
        except Exception as exception:
            logging.error(f'[do_submission] {exception=}')
            return Response({'info': 'something went wrong, please roast yjp.'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'submission_id': submission.id})
