from api.resources import course_methods, question_methods
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
        return question_methods.create_question(request)
