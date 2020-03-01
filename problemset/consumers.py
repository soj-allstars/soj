from channels.generic.websocket import JsonWebsocketConsumer
from judge.tasks import send_check_request
from problemset.models import Problem, Solution
from common.consts import LanguageEnum, CheckerType
from asgiref.sync import async_to_sync


class CheckSolution(JsonWebsocketConsumer):
    def connect(self):
        if not self.scope["user"].is_authenticated:
            self.close()
            return
        self.accept()

    def receive_json(self, content, **kwargs):  # called by receive
        try:
            problem_id = content['problem_id']

            problem = Problem.objects.get(id=problem_id)
            solution = Solution.objects.get(problem_id=problem_id, is_model_solution=True)

            detail = {
                'channel_name': self.channel_name,
                'problem_id': problem_id,
                'solution_code': solution.code,
                'solution_lang': LanguageEnum(solution.lang).name,
                'time_limit': problem.time_limit,
                'memory_limit': problem.memory_limit,
            }
            if problem.checker_type == CheckerType.special_judge:
                detail['sj_code'] = problem.checker_code
                detail['sj_name'] = f'sj_{problem.id}'

            send_check_request(detail)
        except Exception as ex:
            self.send_json({'ok': False, 'detail': str(ex)})
        else:
            self.send_json({'ok': True})

    def check_send_result(self, event):
        self.send_json(event)


class SubmissionInfo(JsonWebsocketConsumer):
    DETAIL_GROUP_NAME_FMT = "submission_detail_{submission_id}"
    USER_LIST_GROUP_NAME_FMT = "submission_user_{user_id}"
    ALL_LIST_GROUP_NAME_FMT = "submission_all"
    CONTEST_LIST_GROUP_NAME_FMT = 'submission_contest_{contest_id}'

    def connect(self):
        self.accept()

    def receive_json(self, content, **kwargs):  # called by receive
        try:
            msg_type = content['type']
            if msg_type == 'detail':
                submission_id = content['submission_id']

                async_to_sync(self.channel_layer.group_add)(
                    self.DETAIL_GROUP_NAME_FMT.format(submission_id=submission_id),
                    self.channel_name
                )
            elif msg_type == 'user':
                user_id = content['user_id']

                async_to_sync(self.channel_layer.group_add)(
                    self.USER_LIST_GROUP_NAME_FMT.format(user_id=user_id),
                    self.channel_name
                )
            elif msg_type == 'contest':
                if not self.scope["user"].is_authenticated:
                    self.close()
                    return
                contest_id = content['contest_id']

                async_to_sync(self.channel_layer.group_add)(
                    self.CONTEST_LIST_GROUP_NAME_FMT.format(contest_id=contest_id),
                    self.channel_name
                )
            elif msg_type == 'all':
                async_to_sync(self.channel_layer.group_add)(
                    self.ALL_LIST_GROUP_NAME_FMT,
                    self.channel_name
                )
            else:
                raise ValueError(f'unsupported type: {msg_type}')
        except Exception as ex:
            self.send_json({'ok': False, 'detail': str(ex)})
        else:
            self.send_json({'ok': True})

    def submission_send_info(self, event):
        self.send_json(event)
