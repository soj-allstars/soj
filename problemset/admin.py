from django.contrib import admin
from django.contrib import messages
from problemset.models import Problem, TestCase, Solution
from problemset.views import save_input_files
from judge.tasks import send_check_request


class SolutionInline(admin.StackedInline):
    model = Solution
    extra = 0


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'visible')
    inlines = [SolutionInline]
    list_filter = ('visible',)
    actions = ['write_inputs_answers']

    def write_inputs_answers(self, request, problems):
        ok = True
        for p in problems:
            save_input_files(p.id, p.testcase.inputs)
            try:
                send_check_request(p)
            except Exception as ex:
                self.message_user(request, f"problem {p.id} failed to generate answer. {ex}", level=messages.ERROR)
                ok = False
        if ok:
            self.message_user(request, "successfully saved all test case files.")
    write_inputs_answers.short_description = 'generate test case input and answer files'


admin.site.register(Problem, ProblemAdmin)
admin.site.register(TestCase)

# Register your models here.
