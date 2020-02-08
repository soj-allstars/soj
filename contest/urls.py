from django.urls import path
from contest.views import ContestDetail, ContestList, register_contest

urlpatterns = [
    path('contests/', ContestList.as_view()),
    path('contest/<int:pk>/', ContestDetail.as_view()),
    path('contest/register/<int:contest_id>/', register_contest),
]
