from channels.generic.websocket import JsonWebsocketConsumer


class CheckSolution(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        print("hello")

    def send_result(self, event):
        pass
