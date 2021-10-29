from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.utils import IntegrityError
from user.models import UserProfile

import requests



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
        username_exists = get_user_model().objects.filter(username=username).exists()
        if (
            not username_exists
            and settings.COMMUNITY_LOGIN_LINK
            and settings.COMMUNITY_USER_INFO_LINK
        ):
            resp = requests.post(settings.COMMUNITY_LOGIN_LINK, json={'username': username, 'password': password})
            if resp.status_code == 200 and resp.json()['code'] == 1:
                cookies = resp.cookies
                resp = requests.get(settings.COMMUNITY_USER_INFO_LINK, cookies=cookies)
                if resp.status_code == 200:
                    user_info = resp.json()['data']
                    new_user = get_user_model().objects.create_user(username, user_info['mail'], password)
                    new_user.save()
                    UserProfile.objects.create(user=new_user, phone=user_info['tel'])
                    return Response()
        return Response({'detail': '密码不正确' if username_exists else '用户不存在'}, status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response()


@api_view(['GET'])
def global_info(request):
    user = request.user
    is_signed_in = bool(user and user.is_authenticated)
    username = user.username if is_signed_in else None
    return Response({
        'is_signed_in': is_signed_in,
        'username': username,
    })


@api_view(['GET'])
def check_username(request):
    username = request.GET['username']
    return Response({'ok': not get_user_model().objects.filter(username=username).exists()})


@api_view(['POST'])
def user_register(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']

    try:
        validate_email(email)
    except ValidationError as ex:
        return Response({'detail': str(ex)}, status=status.HTTP_403_FORBIDDEN)

    try:
        new_user = get_user_model().objects.create_user(username, email, password)
        new_user.save()
    except IntegrityError:
        return Response({'detail': '用户名重复'}, status=status.HTTP_403_FORBIDDEN)

    return Response()
