from django.contrib import admin
from user.models import UserProfile, Submission


class UserInfoAdmin(admin.ModelAdmin):
    pass


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'user', 'submit_time', 'contest')
    list_filter = ('contest', 'problem', 'user', 'submit_time')


admin.site.register(UserProfile, UserInfoAdmin)
admin.site.register(Submission, SubmissionAdmin)
