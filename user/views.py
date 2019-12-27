from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout


@api_view(['POST'])
def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    keep = request.POST.get('keep')
    if keep:
        keep = keep.lower()

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if keep != 'true':
            request.session.set_expiry(0)
        return Response()
    else:
        return Response({'detail': '用户名或密码不正确'}, status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response()
