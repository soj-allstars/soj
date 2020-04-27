from common.consts import LanguageEnum, CheckerType, VerdictResult, ContestCategory
from common.utils import create_file_to_write
from common.permissions import SubmissionAccessPermission
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
    SerializerMethodField,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from problemset.models import Problem, Solution, TestCase
from contest.models import Contest, ContestProblem
from user.models import Submission
from judge.tasks import send_judge_request
from django.db import transaction
from django.conf import settings


def save_input_files(problem_id, inputs):
    for i, test_case in enumerate(inputs):
        with create_file_to_write(f'{settings.PROBLEM_DATA_DIR}/{problem_id}/{i + 1}.in') as f:
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
        solutions = SolutionSerializer(many=True, read_only=True)

        class Meta:
            model = Problem
            fields = '__all__'

    queryset = Problem.objects.all()
    serializer_class = ProblemAdminSerializer
    permission_classes = [IsAdminUser]


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

        def create(self, validated_data):
            validated_data['checker_type'] = getattr(CheckerType, validated_data['checker_type']).value
            if not validated_data['sample_inputs']:
                validated_data['sample_inputs'] = validated_data['inputs'][:2]
            else:
                validated_data['inputs'] = validated_data['sample_inputs'] + validated_data['inputs']
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

        def to_representation(self, problem):  # used in serializer.data
            return {'problem_id': problem.id}

    serializer_class = ProblemPostSerializer
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProblemPut(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        raise NotImplementedError


@api_view(['POST'])
@permission_classes([IsAdminUser])
def make_problem_visible(request, pid):
    Problem.objects.filter(id=pid).update(visible=True)
    return Response()


class SubmissionDetail(RetrieveAPIView):
    class SubmissionDetailSerializer(ModelSerializer):
        verdict = CharField(source='get_verdict_display')
        lang = CharField(source='get_lang_display')
        desc = SerializerMethodField()

        class Meta:
            model = Submission
            fields = ('verdict', 'memory', 'time', 'submit_time',
                      'code', 'lang', 'desc')  # TODO input and output of last wrong case?

        def get_desc(self, obj):
            if obj.verdict == VerdictResult.CE:
                return obj.desc
            return ""

    queryset = Submission.objects.all()
    serializer_class = SubmissionDetailSerializer
    permission_classes = [SubmissionAccessPermission]


class SubmissionPost(APIView):  # legacy code. TODO: refactor to use GenericView
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        problem_id = request.POST['pid']
        code = request.POST['code']
        lang = request.POST['lang']
        contest_id = request.POST.get('contest_id')
        if contest_id:  # only have contest id when the contest is running
            contest = Contest.objects.get(id=contest_id)
            if not contest.is_running:
                return Response({'detail': "you can't submit to a contest that's not running"},
                                status.HTTP_403_FORBIDDEN)
            if contest.category != ContestCategory.OPEN and not contest.is_user_registered(request.user):
                return Response({'detail': "you have no permission to submit to this contest"},
                                status.HTTP_403_FORBIDDEN)
            problem = ContestProblem.objects.get(contest=contest, problem_order=ord(problem_id) - ord('A') + 1).problem
        else:
            problem = Problem.objects.get(id=problem_id)

        submission = Submission()
        submission.user = request.user
        submission.problem_id = problem.id
        submission.code = code
        submission.lang = getattr(LanguageEnum, lang).value
        submission.contest_id = contest_id
        submission.save()

        send_judge_request(problem, submission)

        return Response({'submission_id': submission.id})


class SubmissionList(ListAPIView):
    class SubmissionListSerializer(ModelSerializer):
        verdict = CharField(source='get_verdict_display')
        user = StringRelatedField()
        lang = CharField(source='get_lang_display')

        class Meta:
            model = Submission
            fields = ('id', 'problem_id', 'user_id', 'user', 'verdict', 'submit_time', 'time', 'memory', 'lang')

    queryset = Submission.objects.filter(contest__isnull=True).order_by('-id')
    serializer_class = SubmissionListSerializer
    # TODO override get_queryset to do filtering?
