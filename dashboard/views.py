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
        print 'start db call'
        teacher = Teacher.objects.get(id=request.session['user_id'])
        print 'end db call'
        first_course_id = teacher.courses.all()[0].id
        return redirect('/dashboard/courses/'+str(first_course_id))
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

def exam_index(request):
    #TODO: check user has permissions
    if (request.method == 'GET'):
        try:
            teacher = Teacher.objects.get(id=request.session['user_id'])
            context = {}
            default_exam_id = teacher.courses.all()[0].exams.all()[0].id
            return redirect('dashboard/exams/'+str(default_exam_id)+'?course_num='+str(course_num))
        except Exception, e:
            print e
            return redirect('/dashboard/exams/new')
            #TODO: handle error  properly
    #TODO: handle other methods

# GET, POST, PUT, DELETE
def exam(request):
    #TODO: check user has permissions
    if request.method == 'GET':
        context = {}
        return render(request, 'dashboard/editexam-mockup.html', context)
    elif request.method == 'POST':
        pass
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

# GET, POST, PUT, DELETE
def exam_question(request, exam_num, question_num):
    pass

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

