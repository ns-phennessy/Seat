
def get_course_url():
	return 'dashboard/course.html'
def get_course_context(teacher, course_num, course, courses):
	return {
		'teacher' : teacher,
		'course_num' : course_num,
		'course' : course,
        'courses' : courses
	}

def get_nocourse_url():
	return 'dashboard/nocourse.html'
def get_nocourse_context(teacher):
	return {
		'teacher' : teacher
	}