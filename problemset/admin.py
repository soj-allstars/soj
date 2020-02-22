from django.contrib import admin
from problemset.models import Problem, TestCase, Solution


class TestCaseInline(admin.StackedInline):
    model = TestCase


class SolutionInline(admin.StackedInline):
    model = Solution
    extra = 0


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'visible')
    inlines = [TestCaseInline, SolutionInline]
    list_filter = ('visible',)


admin.site.register(Problem, ProblemAdmin)

# Register your models here.
