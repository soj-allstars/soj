from django.contrib import admin
from user.models import UserInfo, Submission


class UserInfoAdmin(admin.ModelAdmin):
    pass


class SubmissionAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Submission, SubmissionAdmin)
