import requests
import os
import time

hostname = os.getenv('HOSTNAME')
if hostname is None:
    hostname = '127.0.0.1'

def create_session(seq_number: int):
    read_comps = [
        'https://redcap.rwjms.rutgers.edu/surveys/?s=TAT7LTH8MJLYLT84'
        for _ in range(10)
    ]
    url = f'http://{hostname}:8000/sessions'
    params = {
        'seq_number': seq_number,
        'read_comp_link': read_comps[seq_number-1],
        'survey_link': 'https://redcap.rwjms.rutgers.edu/surveys/?s=TAT7LTH8MJLYLT84',
        'is_passthrough': seq_number % 2 == 0
    }
    requests.post(url, params=params)


def create_student(name: str):
    url = f'http://{hostname}:8000/students'
    params = {
        'student_name': name
    }
    requests.post(url, params=params)

time.sleep(5)
create_student('matheus')
create_student('biga')

for i in range(10):
    create_session(i+1)
