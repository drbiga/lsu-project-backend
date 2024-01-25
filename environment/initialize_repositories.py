import requests
import os
import time

hostname = os.getenv('HOSTNAME')
if hostname is None:
    hostname = '127.0.0.1'

def create_session(seq_number: int):
    read_comps = [
        'https://rutgers.ca1.qualtrics.com/jfe/form/SV_8JlFopZFaZ4EE9o',
        'https://rutgers.ca1.qualtrics.com/jfe/form/SV_9FuAL9P1GJf4mZ8',
        'https://rutgers.ca1.qualtrics.com/jfe/form/SV_3a6oimhnjeFBeOq',
        'https://rutgers.ca1.qualtrics.com/jfe/form/SV_73a4YLWIAWxVeWa',
        'https://rutgers.ca1.qualtrics.com/jfe/form/SV_cTvGOOh88lzb4xg',
        'https://rutgers.ca1.qualtrics.com/jfe/form/SV_eG1inuottsKpLtY ',
        'https://rutgers.ca1.qualtrics.com/jfe/form/SV_dpxlSygIoPmAvgq',
        'https://rutgers.ca1.qualtrics.com/jfe/form/SV_e8m1M4QK3H0K8WW',
        'https://rutgers.ca1.qualtrics.com/jfe/form/SV_6zHK9scZObcdPU2',
        'https://rutgers.ca1.qualtrics.com/jfe/form/SV_9mNoIFNwZSQuscK',
    ]
    url = f'http://{hostname}:8000/sessions'
    params = {
        'seq_number': seq_number,
        'read_comp_link': read_comps[seq_number-1],
        'survey_link': 'https://rutgers.ca1.qualtrics.com/jfe/form/SV_8qfsFsMniPKpIsC' if seq_number in [4, 9] else 'https://rutgers.ca1.qualtrics.com/jfe/form/SV_7OmbPs4NypRC0qa',
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
