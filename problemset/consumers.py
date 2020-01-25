from channels.generic.websocket import JsonWebsocketConsumer
from judge.tasks import send_check_request
from problemset.models import Problem, Solution
from common.consts import LanguageEnum, CheckerType


class CheckSolution(JsonWebsocketConsumer):
    def connect(self):
        if not self.scope["user"].is_authenticated:
            self.close()
            return
        self.accept()

    def do_check(self, event):
        problem_id = event['problem_id']
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            self.send_json({'ok': False, 'detail': 'wrong problem id'})
            return
        try:
            solution = Solution.objects.get(problem_id=problem_id, is_model_solution=True)
        except Solution.DoesNotExist:
            self.send_json({'ok': False, 'detail': "solution doesn't exist"})
            return

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
        self.send_json({'ok': True})

    def check_send_result(self, event):
        self.send_json(event)
