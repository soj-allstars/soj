from django.contrib import admin
from problemset.models import Problem, TestCase, Solution


class ProblemAdmin(admin.ModelAdmin):
    pass


class TestCaseAdmin(admin.ModelAdmin):
    pass


class SolutionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Problem, ProblemAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(Solution, SolutionAdmin)

# Register your models here.
