from django.urls import path
from problemset.views import get_problem_detail

urlpatterns = [
    path('detail/', get_problem_detail),
]
