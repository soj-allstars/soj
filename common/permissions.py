from rest_framework.permissions import BasePermission
from contest.models import Contest
from common.consts import ContestCategory


class ContestAccessPermission(BasePermission):
    message = ("Either you didn't register to the contest or "
               "you never entered the contest.")

    # TODO add check for SOLO category
    def has_permission(self, request, view):
        user = request.user
        contest = Contest.objects.get(id=view.kwargs['contest_id'])
        if contest.category != ContestCategory.OPEN and (
                not (user.is_authenticated and user.contest_set.filter(id=contest.id).exists())
        ):
            return False
        return True
