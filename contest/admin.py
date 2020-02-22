from django.contrib import admin
from contest.models import Contest, Standing


class ContestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_time', 'end_time', 'category', 'visible')
    list_filter = ['category', 'visible']
    filter_horizontal = ('problems', 'users')


class StandingAdmin(admin.ModelAdmin):
    list_display = ('contest', 'penalties', 'user')
    list_filter = ['contest', 'user']


admin.site.register(Contest, ContestAdmin)
admin.site.register(Standing, StandingAdmin)
