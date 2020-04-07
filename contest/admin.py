from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from contest.models import Contest, Standing


class ContestProblemInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Contest.problems.through
    extra = 1


class ContestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_time', 'end_time', 'category', 'visible')
    list_filter = ['category', 'visible']
    filter_horizontal = ('users',)
    inlines = [ContestProblemInline]


class StandingAdmin(admin.ModelAdmin):
    list_display = ('contest', 'user')
    list_filter = ['contest']
    search_fields = ['user__username']


admin.site.register(Contest, ContestAdmin)
admin.site.register(Standing, StandingAdmin)
