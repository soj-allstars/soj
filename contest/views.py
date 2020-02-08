from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
)
from rest_framework.serializers import (
    ModelSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from contest.models import Contest
from problemset.views import ProblemList
from common.utils import soj_login_required


class ContestList(ListAPIView):
    class ContestListSerializer(ModelSerializer):
        class Meta:
            model = Contest
            fields = ('id', 'name', 'start_time', 'end_time')

    queryset = Contest.objects.filter(visible=True).order_by('start_time')  # TODO need add index
    serializer_class = ContestListSerializer


class ContestDetail(RetrieveAPIView):
    class ContestDetailSerializer(ModelSerializer):
        problems = ProblemList.ProblemListSerializer(many=True, read_only=True)

        class Meta:
            model = Contest
            fields = ('id', 'name', 'description', 'problems', 'start_time', 'end_time', 'is_running')

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


@soj_login_required
@api_view(['POST'])
def register_contest(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    contest.users.add(request.user)

    return Response()
