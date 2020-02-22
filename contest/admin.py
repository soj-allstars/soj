from django.contrib import admin
from contest.models import Contest, Standing


class ContestAdmin(admin.ModelAdmin):
    pass


class StandingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Contest, ContestAdmin)
admin.site.register(Standing, StandingAdmin)
