
def teacher(request, func):
	# check that the session is valid
	return lambda request: func(request)
	
def student(request, func):
	# check that the session is valid
	return lambda request: func(request)