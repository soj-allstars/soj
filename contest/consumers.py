from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from contest.models import Standing, Contest


class ContestStandings(JsonWebsocketConsumer):
    GROUP_NAME_FMT = 'standings_{}'

    @staticmethod
    def get_sorted_standings(contest_id):
        standings = Standing.objects.filter(contest_id=contest_id)

        result = []
        for standing in standings:
            one_res = {
                'user_id': standing.user_id,
                'username': standing.user.username,
                'solved_number': len(standing.AC_times),
                'total_penalty': standing.total_penalty,
                'AC_times': standing.real_AC_times,
                'wrong_numbers': standing.real_wrong_numbers
            }
            result.append(one_res)

        result.sort(key=lambda x: (-x['solved_number'], x['total_penalty']))
        return result

    def receive_json(self, content, **kwargs):
        try:
            contest_id = content['contest_id']
            contest = Contest.objects.get(id=contest_id)

            standings = self.get_sorted_standings(contest_id)
            message = {'ok': True, 'standings': standings}

            async_to_sync(self.channel_layer.group_add)(
                self.GROUP_NAME_FMT.format(contest_id),
                self.channel_name
            )

        except Exception as ex:
            self.send_json({'ok': False, 'detail': str(ex)})
        else:
            self.send_json(message)
            if not contest.is_running:
                self.disconnect(1000)

    def contest_send_standings(self, event):
        try:
            standings = self.get_sorted_standings(event['contest_id'])
        except Exception as ex:
            self.send_json({'ok': False, 'detail': str(ex)})
        else:
            self.send_json({'ok': True, 'standings': standings})
