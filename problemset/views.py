from common.consts import LanguageEnum, VerdictResult
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveDestroyAPIView,
    RetrieveAPIView,
    ListAPIView,
)
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
    CharField,
)
from problemset.models import Problem
from user.models import Submission
from judge.tasks import send_judge_request
import logging


class ProblemDetail(RetrieveDestroyAPIView):
    class ProblemDetailSerializer(ModelSerializer):
        class Meta:
            model = Problem
            fields = ('title', 'time_limit', 'memory_limit', 'description',
                      'sample_inputs', 'sample_outputs', 'note')

    queryset = Problem.objects.all()
    serializer_class = ProblemDetailSerializer


class ProblemList(ListAPIView):
    class ProblemListSerializer(ModelSerializer):
        class Meta:
            model = Problem
            fields = ('id', 'title')

    queryset = Problem.objects.all()
    serializer_class = ProblemListSerializer


class SubmissionDetail(RetrieveAPIView):
    class SubmissionDetailSerializer(ModelSerializer):
        verdict = SerializerMethodField()
        lang = CharField(source='get_lang_display')

        class Meta:
            model = Submission
            fields = ('verdict', 'memory', 'time', 'submit_time',
                      'code', 'lang', 'outputs')

        def get_verdict(self, obj):
            return VerdictResult(obj.verdict).name if obj.verdict is not None else 'PENDING'

    queryset = Submission.objects.all()
    serializer_class = SubmissionDetailSerializer


class SubmissionPost(APIView):
    def post(self, request):
        problem_id = request.POST['pid']
        code = request.POST['code']
        lang = request.POST['lang']

        problem = Problem.objects.get(id=problem_id)

        try:
            submission = Submission()
            submission.user = request.user
            submission.problem_id = problem_id
            submission.code = code
            submission.lang = getattr(LanguageEnum, lang).value
            submission.save()

            send_judge_request(problem, submission)
        except Exception as exception:
            logging.error(f'[SubmissionPost] {exception=}')
            return Response({'detail': 'something went wrong, please roast yjp.'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'submission_id': submission.id})


class SubmissionList(ListAPIView):
    class SubmissionListSerializer(ModelSerializer):
        verdict = SerializerMethodField()
        user = StringRelatedField()

        class Meta:
            model = Submission
            fields = ('id', 'problem_id', 'user', 'verdict', 'submit_time', 'time', 'memory')

        def get_verdict(self, obj):
            return VerdictResult(obj.verdict).name if obj.verdict is not None else 'PENDING'

    queryset = Submission.objects.all()
    serializer_class = SubmissionListSerializer
