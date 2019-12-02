from django.http.response import JsonResponse
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from problemset.models import Problem


class QuestionDetail(TemplateView):
    template_name = 'index.html'


@api_view(['GET'])
def get_problem_detail(request):
    problem_id = request.GET.get('pid')
    if not problem_id:
        return JsonResponse({'success': False, 'info': 'Kawaii make MY day!'})

    try:
        problem = Problem.objects.get(id=problem_id)
    except Problem.DoesNotExist:
        return JsonResponse({'success': False, 'info': 'Invalid problem id'})
    return JsonResponse({
        'success': True,
        'title': problem.title,
        'time_limit': problem.time_limit,
        'memory_limit': problem.memory_limit,
        'description': problem.description,
        'sample_inputs': problem.sample_inputs,
        'sample_outputs': problem.sample_outputs,
        'note': problem.note,
    })
