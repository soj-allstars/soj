from django.contrib import admin
from django.contrib import messages
from django.conf import settings
from problemset.models import Problem, Solution
from judge.tasks import send_check_request

import shutil


class SolutionInline(admin.StackedInline):
    model = Solution
    extra = 0


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'checker_type', 'visible')
    inlines = [SolutionInline]
    list_filter = ('visible',)
    actions = ['write_inputs_answers', 'mark_as_visible', 'mark_as_invisible']

    def write_inputs_answers(self, request, problems):
        ok = True
        for p in problems:
            try:
                send_check_request(p)
            except Exception as ex:
                self.message_user(request, f"problem {p.id} failed to generate answer. {ex}", level=messages.ERROR)
                ok = False
        if ok:
            self.message_user(request, "successfully send all requests.")
    write_inputs_answers.short_description = 'Generate answer files'

    def mark_as_visible(self, request, problems):
        problems.update(visible=True)
        self.message_user(request, 'done.')
    mark_as_visible.short_description = 'Mark problems as visible'

    def mark_as_invisible(self, request, problems):
        problems.update(visible=False)
        self.message_user(request, 'done.')
    mark_as_invisible.short_description = 'Mark problems as invisible'

    def delete_model(self, request, obj) -> None:
        problem_id = obj.id
        super().delete_model(request, obj)
        shutil.rmtree(f'{settings.PROBLEM_DATA_DIR}/{problem_id}', ignore_errors=True)

    def delete_queryset(self, request, queryset) -> None:
        problem_ids = [obj.id for obj in queryset]
        super().delete_queryset(request, queryset)
        for problem_id in problem_ids:
            shutil.rmtree(f'{settings.PROBLEM_DATA_DIR}/{problem_id}', ignore_errors=True)


admin.site.register(Problem, ProblemAdmin)
