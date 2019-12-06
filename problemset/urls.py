from django.urls import path
from problemset.views import get_problem_detail, do_submission

urlpatterns = [
    path('detail/', get_problem_detail),
    path('submit/', do_submission),
]
