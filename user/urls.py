from django.urls import path, include
from user.views import user_login, user_logout

urlpatterns = [
    path('user/login/', user_login),
    path('user/logout/', user_logout),
]
