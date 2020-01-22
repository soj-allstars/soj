from django.urls import path
from judge.views import judge_finished, check_finished

urlpatterns = [
    path('judge/result/', judge_finished),
    path('judge/solution-checker-result/', check_finished),
]
