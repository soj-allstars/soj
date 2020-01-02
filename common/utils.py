from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from django.http import HttpRequest


def soj_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        actual_request = request
        if not isinstance(actual_request, HttpRequest):
            actual_request = args[0]
        if actual_request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return Response({'detail': '没登录就想搞事情？我记在日志里了(  ^ω^)'}, status=HTTP_403_FORBIDDEN)
    return _wrapped_view
