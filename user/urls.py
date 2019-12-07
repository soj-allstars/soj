from django.urls import path
from user.views import get_user_submission

urlpatterns = [
    path('detail/', get_user_submission),
]
