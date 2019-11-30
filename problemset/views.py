from django.shortcuts import render
from django.views.generic import TemplateView


class QuestionDetail(TemplateView):
    template_name = 'index.html'
