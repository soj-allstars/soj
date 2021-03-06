from django.urls import path
from contest.views import (
    ContestDetail,
    ContestList,
    register_contest,
    unregister_contest,
    verify_password,
    ContestSubmissionList,
    ContestProblemDetail
)
from contest.consumers import ContestStandings

urlpatterns = [
    path('contests/', ContestList.as_view()),
    path('contest/<int:contest_id>/', ContestDetail.as_view()),
    path('contest/register/<int:contest_id>/', register_contest),
    path('contest/unregister/<int:contest_id>/', unregister_contest),
    path('contest/let-me-in/<int:contest_id>/', verify_password),
    path('contest/submissions/<int:contest_id>/', ContestSubmissionList.as_view()),
    path('contest/problem/<int:contest_id>/<str:problem_no>/', ContestProblemDetail.as_view()),
]

websocket_urlpatterns = [
    path('ws/contest/standings/', ContestStandings),
]
