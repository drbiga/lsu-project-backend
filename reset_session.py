import shelve


def fix():
	with shelve.open('data/students.shelve') as db:
		amy = db['amy']
		sessions = amy['session_executions']
		sessions.pop()
		db['amy'] = amy

def check():
	with shelve.open('data/students.shelve') as db:
		amy = db['amy']

		print(amy)


check()
