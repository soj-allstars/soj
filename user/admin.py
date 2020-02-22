from django.contrib import admin
from user.models import UserInfo, Submission


class UserInfoAdmin(admin.ModelAdmin):
    pass


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'user', 'submit_time', 'contest')
    list_filter = ('contest', 'problem', 'user', 'submit_time')


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Submission, SubmissionAdmin)
