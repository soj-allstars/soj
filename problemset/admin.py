from django import forms
from django.contrib import admin
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ValidationError
from problemset.models import Problem, Solution
from problemset.views import save_input_files
from judge.tasks import send_check_request

import json
import os
import shutil


def get_problem_test_cases_as_json(problem_id: int):
    test_cases = []
    idx = 1
    while True:
        input_file = f'{settings.PROBLEM_DATA_DIR}/{problem_id}/{idx}.in'
        if not os.path.isfile(input_file):
            break
        with open(input_file, 'r') as f:
            test_cases.append(f.read())
        idx += 1
    return json.dumps(test_cases)


class SolutionInline(admin.StackedInline):
    model = Solution
    extra = 0


class ProblemForm(forms.ModelForm):
    test_cases = forms.CharField(required=True, widget=forms.Textarea)

    def clean_test_cases(self):
        test_cases = self.cleaned_data['test_cases']
        try:
            obj = json.loads(test_cases)
        except json.JSONDecodeError:
            raise ValidationError("Not a valid JSON value!")
        if type(obj) is not list:
            raise ValidationError("Not a valid JSON list!")
        for ele in obj:
            if type(ele) is not str:
                raise ValidationError("Every element should be a string!")
        return obj


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'checker_type', 'visible')
    inlines = [SolutionInline]
    list_filter = ('visible',)
    actions = ['write_inputs_answers', 'mark_as_visible', 'mark_as_invisible']
    form = ProblemForm
    fields = (
        'id', 'title', 'visible', 'description', 'time_limit', 'memory_limit', 'sample_inputs',
        'sample_outputs', 'note', 'checker_type', 'checker_code', 'test_cases',
    )
    readonly_fields = ('id',)

    def get_form(self, request, obj, change, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        if obj:
            form.base_fields['test_cases'].initial = get_problem_test_cases_as_json(obj.id)
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        test_cases = form.cleaned_data['test_cases']
        save_input_files(obj.id, test_cases)

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
