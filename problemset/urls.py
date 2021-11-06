from django.urls import path
from problemset.views import (
    ProblemDetail,
    SubmissionDetail,
    ProblemList,
    SubmissionList,
    SubmissionPost,
    ProblemPost,
    make_problem_visible,
    ProblemAdminDetail,
    ProblemPut,
)
from problemset.consumers import CheckSolution, SubmissionInfo

urlpatterns = [
    path('problem/<int:pk>/', ProblemDetail.as_view()),
    path('problem/admin/<int:pk>/', ProblemAdminDetail.as_view()),
    path('problems/', ProblemList.as_view()),
    path('submission/<int:pk>/', SubmissionDetail.as_view()),
    path('submission/', SubmissionPost.as_view()),
    path('submissions/', SubmissionList.as_view()),
    path('problem/save/', ProblemPost.as_view()),
    path('problem/save/<int:pk>/', ProblemPut.as_view()),
    path('problem/publish/<int:pid>/', make_problem_visible),
]

websocket_urlpatterns = [
    path('ws/problem/check/', CheckSolution),
    path('ws/submission/', SubmissionInfo),
]
