from django.contrib import admin
from user.models import UserProfile, Submission
from judge.tasks import send_judge_request


class UserInfoAdmin(admin.ModelAdmin):
    pass


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'user', 'verdict', 'submit_time', 'contest')
    list_filter = ('verdict', 'contest', 'submit_time', 'lang')
    search_fields = ('user__username', 'problem__title')
    actions = ['rejudge']

    def rejudge(self, request, submissions):
        for s in submissions:
            send_judge_request(s.problem, s)
        self.message_user(request, "successfully send rejudge requests.")
    rejudge.short_description = 'rejudge submissions'


admin.site.register(UserProfile, UserInfoAdmin)
admin.site.register(Submission, SubmissionAdmin)
