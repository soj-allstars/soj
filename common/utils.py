from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.request import Request
import os


def create_file_to_write(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')


def soj_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        actual_request = request
        if not isinstance(actual_request, Request):
            actual_request = args[0]
        if actual_request.user.is_authenticated:
            # if decorated func is a method, then request is self, args[0] is actual request
            return view_func(request, *args, **kwargs)
        return Response({'detail': '没登录就想搞事情？我记在日志里了(  ^ω^)'}, status=HTTP_403_FORBIDDEN)
    return _wrapped_view


def soj_superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        actual_request = request
        if not isinstance(actual_request, Request):
            actual_request = args[0]
        if actual_request.user.is_superuser:
            # if decorated func is a method, then request is self, args[0] is actual request
            return view_func(request, *args, **kwargs)
        return Response({'detail': '(  ^ω^)'}, status=HTTP_403_FORBIDDEN)
    return _wrapped_view
