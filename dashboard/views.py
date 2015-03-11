#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import date
from dashboard.models import Teacher,Course,Exam,Question
from django.http import JsonResponse

#TODO: remove this whene there isa real db
def initialize_database_objects():
    default_teacher = Teacher.objects.get_or_create(name="joe", email="guilliamsd@mizzou.edu")[0]
    default_teacher.save()
    default_courses = [
        Course.objects.get_or_create(id=1,name="CS2050 - Algorithm Design II"),
        Course.objects.get_or_create(id=2,name="ECE 1210 - Digital Logic"),
        Course.objects.get_or_create(id=3,name="CS1000 - Introduction to Computer Science")
    ]
    default_questions = [
        Question.objects.get_or_create(id=1,category="Multiple Choice",text="Who's your daddy?"),
        Question.objects.get_or_create(id=2,category="True/False",text="What is real?"),
        Question.objects.get_or_create(id=3,category="Short Answer",text="Explain.")
    ]
    default_exams= [
        Exam.objects.get_or_create(id=1, name='Ex 1'),
        Exam.objects.get_or_create(id=2, name='Ex 2'),
    ]
    for i in range(len(default_courses)):
        for j in range(len(default_exams)):
            default_exams[j][0].save()
            for k in range(len(default_questions)):
                default_questions[k][0].save()
                default_exams[j][0].questions.add(default_questions[k][0])
            default_courses[i][0].exams.add(default_exams[j][0])
        default_courses[i][0].save()
        default_teacher.courses.add(default_courses[i][0])
    default_teacher.save()

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
            initialize_database_objects()
            teacher = Teacher.objects.get(id=request.session['user_id'])
            course = Course.objects.get(id=courseNum)
        except Course.DoesNotExist:
            #TODO: handle error in the view
            raise Exception("course with specified coursname failed to load")
        context = {
            'teacher': teacher,
            'courseNum': courseNum,
            'course': course
            }
        return render(request, 'dashboard/course.html', context)
    elif request.method == 'POST':
        pass

# GET, POST, PUT, DELETE
def exam(request, exam_num):
    #TODO: check user has permissions
    if request.method == 'GET':
        context = {}
        return render(request, 'dashboard/editexam-mockup.html', context)
    elif request.method == 'POST':
        pass

# GET
def exam_edit(request, exam_num):
    #TODO: check user has permissions
    initialize_database_objects()
    teacher = Teacher.objects.get(id=request.session['user_id'])
    exam = Exam.objects.get(id=exam_num)
    context = { 'teacher': teacher, 'exam': exam }
    return render(request, 'dashboard/exam.html', context)

# GET
def exam_new(request):
    #TODO: check user has permissions
    if request.method == 'GET':
        initialize_database_objects()
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
            new_course = Course.objects.get_or_create(name=request.POST['name'])[0]
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
        
    
