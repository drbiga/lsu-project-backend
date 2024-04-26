import shelve


def fix(name: str):
	with shelve.open('data/students.shelve') as db:
		student = db[name]
		sessions = student['session_executions']
		sessions.pop()
		db[name] = student

def check(name: str):
	with shelve.open('data/students.shelve') as db:
		student = db[name]

		print(student)

# fix('callen')
check('callen')
