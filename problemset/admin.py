from django.contrib import admin
from problemset.models import Problem, TestCase, Solution


class SolutionInline(admin.StackedInline):
    model = Solution
    extra = 0


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'visible')
    inlines = [SolutionInline]
    list_filter = ('visible',)


admin.site.register(Problem, ProblemAdmin)
admin.site.register(TestCase)

# Register your models here.
