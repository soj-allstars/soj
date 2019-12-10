from django.urls import path
from problemset.views import ProblemDetail, SubmissionDetail, ProblemList, SubmissionList, SubmissionPost

urlpatterns = [
    path('problem/<int:pk>/', ProblemDetail.as_view()),
    path('problems/', ProblemList.as_view()),
    path('submission/<int:pk>/', SubmissionDetail.as_view()),
    path('submission/', SubmissionPost.as_view()),
    path('submissions/', SubmissionList.as_view()),
]
