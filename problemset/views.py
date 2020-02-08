from common.consts import LanguageEnum, VerdictResult, CheckerType
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
)
from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    CharField,
    JSONField,
)
from rest_framework.decorators import api_view
from problemset.models import Problem, Solution, TestCase
from contest.models import Contest
from user.models import Submission
from judge.tasks import send_judge_request
import logging
from common.utils import soj_login_required, create_file_to_write, soj_superuser_required
from django.db import transaction
from django.conf import settings


def save_input_files(problem_id, inputs):
    for i, test_case in enumerate(inputs):
        with create_file_to_write(f'{settings.PROBLEM_DATA_DIR}/{problem_id}/{i + 1}_in') as f:
            f.write(test_case)


class ProblemDetail(RetrieveAPIView):
    class ProblemDetailSerializer(ModelSerializer):
        class Meta:
            model = Problem
            fields = ('title', 'time_limit', 'memory_limit', 'description',
                      'sample_inputs', 'sample_outputs', 'note')

    queryset = Problem.objects.filter(visible=True)
    serializer_class = ProblemDetailSerializer


class ProblemAdminDetail(RetrieveAPIView):
    class ProblemAdminSerializer(ModelSerializer):
        class SolutionSerializer(ModelSerializer):
            lang = CharField(source='get_lang_display')

            class Meta:
                model = Solution
                fields = ('code', 'lang', 'is_model_solution')

        checker_type = CharField(source='get_checker_type_display')
        inputs = JSONField(source='testcase.inputs')
        solutions = SolutionSerializer(many=True, read_only=True)

        class Meta:
            model = Problem
            fields = '__all__'

    queryset = Problem.objects.all()
    serializer_class = ProblemAdminSerializer

    @soj_superuser_required
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProblemList(ListAPIView):
    class ProblemListSerializer(ModelSerializer):
        class Meta:
            model = Problem
            fields = ('id', 'title')

    queryset = Problem.objects.filter(visible=True).order_by('id')
    serializer_class = ProblemListSerializer


class ProblemPost(CreateAPIView):
    class ProblemPostSerializer(ModelSerializer):
        inputs = JSONField()
        sample_inputs = JSONField()
        solution_code = CharField()
        solution_lang = CharField()
        checker_type = CharField()
        checker_code = CharField(allow_blank=True)

        class Meta:
            model = Problem
            fields = ('title', 'description', 'time_limit', 'memory_limit', 'note',
                      'sample_inputs', 'checker_type', 'inputs', 'checker_code',
                      'solution_code', 'solution_lang')

        def create(self, validated_data):  # TODO if sample_inputs get sample_outputs
            validated_data['checker_type'] = getattr(CheckerType, validated_data['checker_type']).value
            if not validated_data['sample_inputs']:
                validated_data['sample_inputs'] = validated_data['inputs'][:2]
            inputs = validated_data.pop('inputs')
            solution_code = validated_data.pop('solution_code')
            solution_lang = validated_data.pop('solution_lang')

            problem = Problem(**validated_data)
            problem.save()
            test_case = TestCase(problem=problem, inputs=inputs, expected_outputs="")
            solution = Solution(problem=problem, code=solution_code,
                                lang=getattr(LanguageEnum, solution_lang).value, is_model_solution=True)
            test_case.save()
            solution.save()

            save_input_files(problem.id, inputs)

            return problem

    serializer_class = ProblemPostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        problem = serializer.save()

        return Response({'problem_id': problem.id})

    @soj_login_required
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)


class ProblemPut(APIView):
    @soj_login_required
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        raise NotImplementedError


@soj_login_required
@api_view(['POST'])
def make_problem_visible(request, pid):
    problem = Problem.objects.get(id=pid)
    problem.visible = True
    problem.save(update_fields=['visible'])

    return Response()


class SubmissionDetail(RetrieveAPIView):
    class SubmissionDetailSerializer(ModelSerializer):
        verdict = CharField(source='get_verdict_display')
        lang = CharField(source='get_lang_display')

        class Meta:
            model = Submission
            fields = ('verdict', 'memory', 'time', 'submit_time',
                      'code', 'lang', 'outputs')

    queryset = Submission.objects.all()
    serializer_class = SubmissionDetailSerializer


class SubmissionPost(APIView):
    @soj_login_required
    @transaction.atomic
    def post(self, request):
        problem_id = request.POST['pid']
        code = request.POST['code']
        lang = request.POST['lang']
        contest_id = request.POST.get('contest_id')
        if contest_id:
            contest = Contest.objects.get(id=contest_id)
            if not contest.is_running:
                return Response({'detail': "you can't submit to a contest that's not running"},
                                status.HTTP_403_FORBIDDEN)

        problem = Problem.objects.get(id=problem_id)

        try:
            submission = Submission()
            submission.user = request.user
            submission.problem_id = problem_id
            submission.code = code
            submission.lang = getattr(LanguageEnum, lang).value
            submission.contest_id = contest_id
            submission.save()

            send_judge_request(problem, submission)
        except Exception as exception:
            logging.error(f'[SubmissionPost] {exception=}')
            return Response({'detail': 'something went wrong, please roast yjp.'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'submission_id': submission.id})


class SubmissionList(ListAPIView):
    class SubmissionListSerializer(ModelSerializer):
        verdict = CharField(source='get_verdict_display')
        user = StringRelatedField()

        class Meta:
            model = Submission
            fields = ('id', 'problem_id', 'user_id', 'user', 'verdict', 'submit_time', 'time', 'memory')

    queryset = Submission.objects.all().order_by('-id')
    serializer_class = SubmissionListSerializer
