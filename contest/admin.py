from django.contrib import admin
from contest.models import Contest


class ContestAdmin(admin.ModelAdmin):
    pass


admin.site.register(Contest, ContestAdmin)
