from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
)
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from contest.models import Contest
from problemset.views import ProblemList
from common.utils import soj_login_required
from common.consts import ContestCategory


class ContestList(ListAPIView):
    class ContestListSerializer(ModelSerializer):
        category = CharField(source='get_category_display')

        class Meta:
            model = Contest
            fields = ('id', 'name', 'start_time', 'end_time', 'is_running', 'category')

    queryset = Contest.objects.filter(visible=True).order_by('start_time')  # TODO need add index
    serializer_class = ContestListSerializer


class ContestDetail(RetrieveAPIView):
    class ContestDetailSerializer(ModelSerializer):
        problems = ProblemList.ProblemListSerializer(many=True, read_only=True)
        category = CharField(source='get_category_display')

        class Meta:
            model = Contest
            fields = ('id', 'name', 'description', 'problems',
                      'start_time', 'end_time', 'is_running', 'category')

    queryset = Contest.objects.filter(visible=True)
    serializer_class = ContestDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['registered'] = (
            request.user.is_authenticated and
            request.user.contest_set.filter(id=instance.id).exists()
        )
        return Response(data)


@api_view(['POST'])
@soj_login_required
def verify_password(request, contest_id):
    password = request.POST['password']
    contest = Contest.objects.get(id=contest_id)
    if contest.category != ContestCategory.PRIVATE:
        return Response({'detail': "干"}, status=status.HTTP_403_FORBIDDEN)

    return Response({'ok': password == contest.password})


@api_view(['POST'])
@soj_login_required
def register_contest(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    if contest.category != ContestCategory.REGISTER:
        return Response({'detail': "你想干嘛"}, status=status.HTTP_403_FORBIDDEN)
    if contest.is_started:
        return Response({'detail': "开始了不准 register！"}, status=status.HTTP_403_FORBIDDEN)

    contest.users.add(request.user)

    return Response()


@api_view(['POST'])
@soj_login_required
def unregister_contest(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    if contest.category != ContestCategory.REGISTER:
        return Response({'detail': "你想干嘛"}, status=status.HTTP_403_FORBIDDEN)
    if contest.is_started:
        return Response({'detail': "开始了不准 unregister！"}, status=status.HTTP_403_FORBIDDEN)

    contest.users.remove(request.user)

    return Response()
