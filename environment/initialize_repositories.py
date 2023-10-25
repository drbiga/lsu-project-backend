import requests

import time

def create_session(seq_number: int):
    url = 'http://session:8000/sessions'
    params = {
        'seq_number': seq_number,
        'read_comp_link': 'https://rutgers.ca1.qualtrics.com/jfe/form/SV_8JlFopZFaZ4EE9o',
        'survey_link': 'https://rutgers.ca1.qualtrics.com/jfe/form/SV_8JlFopZFaZ4EE9o'
    }
    requests.post(url, params=params)


def create_student(name: str):
    url = 'http://session:8000/students'
    params = {
        'student_name': name
    }
    requests.post(url, params=params)

time.sleep(5)
create_student('matheus')
create_student('biga')

for i in range(10):
    create_session(i+1)
