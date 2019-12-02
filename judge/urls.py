from django.urls import path
from judge.views import judge_finished

urlpatterns = [
    path('send-result/', judge_finished),
]
