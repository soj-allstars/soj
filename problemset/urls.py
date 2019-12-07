from django.urls import path
from problemset.views import ProblemView, SubmissionView

urlpatterns = [
    path('problem/', ProblemView.as_view()),
    path('submission/', SubmissionView.as_view()),
]
