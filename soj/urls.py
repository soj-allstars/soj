"""soj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from problemset.urls import urlpatterns as problemset_apis
from judge.urls import urlpatterns as judge_apis
from user.urls import urlpatterns as user_apis
from contest.urls import urlpatterns as contest_apis


api_patterns = problemset_apis + judge_apis + user_apis + contest_apis

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/', include(api_patterns)),
]
