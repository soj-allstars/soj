import socket
from django.conf import settings
import logging


def send_judge_request(problem, submission):
    try:
        sock = socket.create_connection(settings.JUDGER_ADDR)
    except socket.timeout:
        logging.error(f'cannot connect to judger')
        return
    pass
