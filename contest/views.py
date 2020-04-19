from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
)
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    StringRelatedField,
    SerializerMethodField,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from contest.models import Contest, ContestProblem
from common.consts import ContestCategory
from common.permissions import ContestAccessPermission
from user.models import Submission
from problemset.views import ProblemDetail


class ContestList(ListAPIView):
    class ContestListSerializer(ModelSerializer):
        category = CharField(source='get_category_display')
        registered = SerializerMethodField()

        class Meta:
            model = Contest
            fields = ('id', 'name', 'start_time', 'end_time', 'is_running', 'category', 'registered')

        def get_registered(self, obj):
            user = self.context['request'].user
            return obj.is_user_registered(user)

    queryset = Contest.objects.filter(visible=True).order_by('-start_time')
    serializer_class = ContestListSerializer


class ContestDetail(RetrieveAPIView):
    class ContestDetailSerializer(ModelSerializer):
        problems = SerializerMethodField()
        category = CharField(source='get_category_display')
        registered = SerializerMethodField()

        class Meta:
            model = Contest
            fields = ('id', 'name', 'description', 'problems',
                      'start_time', 'end_time', 'is_running', 'category', 'registered')

        def get_problems(self, obj):
            res = []
            contest_problems = ContestProblem.objects.select_related('problem').filter(contest=obj).order_by('problem_order')
            for cp in contest_problems:
                res.append({'id': cp.problem_order, 'title': cp.problem.title})
            return res

        def get_registered(self, obj):
            user = self.context['request'].user
            return obj.is_user_registered(user)

    queryset = Contest.objects.filter(visible=True)
    serializer_class = ContestDetailSerializer
    permission_classes = [ContestAccessPermission]
    lookup_url_kwarg = 'contest_id'


class ContestProblemDetail(RetrieveAPIView):
    def get_object(self):
        queryset = self.get_queryset()

        problem_order = ord(self.kwargs['problem_no']) - ord('A') + 1
        contest_id = self.kwargs['contest_id']

        obj = get_object_or_404(queryset, contest_id=contest_id, problem_order=problem_order)
        self.check_object_permissions(self.request, obj)
        return obj.problem

    queryset = ContestProblem.objects.all()
    serializer_class = ProblemDetail.ProblemDetailSerializer
    permission_classes = [ContestAccessPermission]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_password(request, contest_id):
    password = request.POST['password']
    contest = Contest.objects.get(id=contest_id)
    if contest.category != ContestCategory.PRIVATE:
        return Response({'detail': "wrong contest category"}, status=status.HTTP_403_FORBIDDEN)

    ok = (password == contest.password)
    if ok:
        # once a user entered the password, he/she can access the contest without entering the password any more
        contest.users.add(request.user)

    return Response({'ok': ok})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_contest(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    if contest.category != ContestCategory.REGISTER:
        return Response({'detail': "wrong contest category"}, status=status.HTTP_403_FORBIDDEN)
    if contest.is_started:
        return Response({'detail': "不准 register！"}, status=status.HTTP_403_FORBIDDEN)

    contest.users.add(request.user)

    return Response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unregister_contest(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    if contest.category != ContestCategory.REGISTER:
        return Response({'detail': "wrong contest category"}, status=status.HTTP_403_FORBIDDEN)
    if contest.is_started:
        return Response({'detail': "不准 unregister！"}, status=status.HTTP_403_FORBIDDEN)

    contest.users.remove(request.user)

    return Response()


class ContestSubmissionList(ListAPIView):
    class SubmissionListSerializer(ModelSerializer):
        verdict = CharField(source='get_verdict_display')
        user = StringRelatedField()
        lang = CharField(source='get_lang_display')
        problem_no = SerializerMethodField()

        class Meta:
            model = Submission
            fields = ('id', 'problem_no', 'user_id', 'user', 'verdict', 'submit_time', 'time', 'memory', 'lang')

        def get_problem_no(self, obj):
            problem_id = obj.problem_id
            problem_order = ContestProblem.objects.get(contest_id=obj.contest_id, problem_id=problem_id).problem_order
            return chr(ord('A') + problem_order - 1)

    serializer_class = SubmissionListSerializer
    permission_classes = [ContestAccessPermission]

    def get_queryset(self):
        contest_id = self.kwargs['contest_id']
        filter_args = {'contest_id': contest_id}
        submissions = Submission.objects.filter(**filter_args)
        return submissions
