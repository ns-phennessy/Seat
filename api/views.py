from api.resources import course_methods, question_methods, exam_methods, token_methods, token_validation, submission_methods, grade_methods
from django.http import HttpResponseNotAllowed

def course(request, course_id = None):
    if request.method == 'POST':
        return course_methods.create_course(request)
    elif request.method == 'PUT':
        return course_methods.update_course(request)
    elif request.method == 'DELETE':
        return course_methods.delete_course(request)
    elif request.method == 'GET':
        return course_methods.get_course(request, course_id)
    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'POST', 'DELETE'])

def exam(request):
    if request.method == 'POST':
        return exam_methods.create_exam(request)
    elif request.method == 'PUT':
        return exam_methods.update_exam(request)
    elif request.method == 'DELETE':
        return exam_methods.delete_exam(request)
    elif request.method == 'GET':
        return exam_methods.get_exam(request)
    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'POST', 'DELETE'])

def question(request):
    if request.method == 'POST':
        return question_methods.upsert_question(request)
    elif request.method == 'DELETE':
        return question_methods.delete_question(request)
    elif request.method == 'GET':
        return question_methods.get_question(request)
    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'DELETE'])

def token(request):
    if request.method == 'POST':
        return token_methods.create_token(request)
    elif request.method == 'PUT':
        return token_methods.update_token(request)
    elif request.method == 'DELETE':
        return token_methods.delete_token(request)
    elif request.method == 'GET':
        return token_methods.get_token(request)
    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'POST', 'DELETE'])


def validate_token(request):
    return token_validation.validate_token(request)

def submission(request):
    if request.method == 'POST':
        return submission_methods.submit(request)
    if request.method == 'PUT':
        return submission_methods.manual_grade(request)
    return HttpResponseNotAllowed(['PUT', 'POST'])

def grade(request):
    return grade_methods.grade(request)