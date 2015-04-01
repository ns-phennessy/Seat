#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import date
from dashboard.models import Teacher,Course,Exam,Question
from django.http import JsonResponse

class MyExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if not isinstance(exception, SomeExceptionType):
            return None
        return HttpResponse('some message')


def show404(request):
	return render(request, 'dashboard/404.html')

def dashboard_index(request):
    #TODO: check the user has permissions (is a teacher)
    #TODO: check for unsupported methods
    try:
        teacher = Teacher.objects.get(id=request.session['user_id'])
        if (teacher.courses.count() > 0):
            first_course = teacher.courses.all()[0]
            return redirect('/dashboard/courses/'+str(first_course.id))
        context = {
            'teacher': teacher,
        }
        return render(request, 'dashboard/nocourse.html', context)
    except Exception, e:
        print e
        return redirect('/logout?message=therewasanerror')#TODO handle this more rightly

def course(request, courseNum):
    if 'user_id' not in request.session:
        return redirect('/login/')
    if request.method == 'GET':
        #TODO: check user has permissions
		try:
			teacher = Teacher.objects.get(id=request.session['user_id'])
			course = Course.objects.get(id=courseNum)
		except Course.DoesNotExist:
			raise Exception("Course with specified coursname failed to load")

		else:
			context = {
				'teacher': teacher,
				'courseNum': int(courseNum),
				'course': course
			}
			return render(request, 'dashboard/course.html', context)

    elif request.method == 'POST':
        pass
    #TODO: handle other methods

# POST
def course_new(request):
    #TODO: check user has permissions
    if request.method == 'POST':
        try:
            new_course = Course.objects.create(name=request.POST['name'])
            teacher = Teacher.objects.get(id=request.session['user_id'])
            new_course.save()
            teacher.courses.add(new_course)
            teacher.save()
            return JsonResponse({ 'success' : True, 'error' : False, 'id' : str(new_course.id) })
        except Exception, e:
            #TODO: handle error case properly, still haven't hit enough of these to decide yet how
            print e
            return JsonResponse({ 'success' : False, 'error' : True,  'message' : str(e) })
    #TODO: handle else condition

# GET?, POST, PUT, DELETE
def exam(request, exam_num):
    #TODO: check user has permissions
    exam = Exam.objects.get(id=exam_num)
    if request.method == 'DELETE':
        exam.delete()
        return JsonResponse({ 'success' : True, 'error' : False })
    #TODO: handle other methods

# GET
def exam_edit(request, exam_num):
    #TODO: check user has permissions
    teacher = Teacher.objects.get(id=request.session['user_id'])
    exam = Exam.objects.get(id=exam_num)
    context = { 'teacher': teacher, 'exam': exam }
    return render(request, 'dashboard/exam.html', context)

# GET
def exam_new(request):
    #TODO: check user has permissions
    if request.method == 'GET':
        teacher = Teacher.objects.get(id=request.session['user_id'])
        context = { 'teacher': teacher }
        return render(request, 'dashboard/exam.html', context)
    #TODO: handle else condition

question_urls = { 'Multiple Choice': 'dashboard/multiple-choice.html'
                , 'True/False': 'dashboard/true-false.html'
                , 'Short Answer': 'dashboard/short-answer.html'
                , 'Essay': ''
                }

# GET
def questions_index(request, exam_id):
    if request.method == 'GET':
        exam = Exam.objects.get(id=exam_id)
        context = { 'exam': exam }
        return render(request, 'dashboard/questions.html', context)

# GET, POST, PUT, DELETE
def question(request, question_id):
    #TODO: check user has permissions
    if request.method == 'GET':
        question = Question.objects.get(id=question_id)
        context = { 'question': question }
        return render(request, question_urls[question.category], context)
