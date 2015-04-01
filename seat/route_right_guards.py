
def verify_teacher_and_execute_func(request, func):
	# if invalid return something else
	return func(request)

def verify_student_and_execute_func(request, func):
	# if invalid return something else
	return func()

def teacher(func):
	return lambda request: verify_teacher_and_execute_func(request, func)
	
def student(func):
	return lambda request: verify_student_and_execute_func(request)