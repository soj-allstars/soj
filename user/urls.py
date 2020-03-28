from django.urls import path
from user.views import user_login, user_logout, check_username, user_register, global_info

urlpatterns = [
    path('user/login/', user_login),
    path('user/logout/', user_logout),
    path('user/register/', user_register),
    path('user/check-username/', check_username),
    path('global-info/', global_info),
]
