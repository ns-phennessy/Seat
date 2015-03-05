#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from datetime import date
from dashboard.models import Teacher
from dashboard.models import Course
from dashboard.models import Exam


# fake exam data
# exam1 = {
#     'name': 'Exam 1',
#     'updated_at': date(2015, 2, 12),
#     'questions': [{} for i in range(15)],
#     'submissions': [{} for i in range(30)],
#     }
# exam2 = {
#     'name': 'Exam 2',
#     'updated_at': date(2015, 3, 3),
#     'questions': [{} for i in range(17)],
#     'submissions': [{} for i in range(29)],
#     }
# exams = [exam1, exam2]

# # fake teacher data
# cs2050 = {'id': '1', 'name': 'CS2050 - Algorithm Design II', 'exams': exams}
# teacher = {'name': 'Joe Teach'}

def get_session():
    #hacky as fuck initialize db
    default_teacher = Teacher.objects.get_or_create(name="joe", email="guilliamsd@mizzou.edu")[0]
    default_teacher.save()
    default_courses = [
        Course.objects.get_or_create(id=1,name="CS2050 - Algorithm Design II"),
        Course.objects.get_or_create(id=2,name="ECE 1210 - Digital Logic"),
        Course.objects.get_or_create(id=3,name="CS1000 - Introduction to Computer Science")
    ]
    default_exams= [
        Exam.objects.get_or_create(id=1, name='Ex 1'),
        Exam.objects.get_or_create(id=2, name='Ex 2'),
    ]
    for i in range(len(default_courses)):
        for j in range(len(default_exams)):
            default_exams[j][0].save()
            default_courses[i][0].exams.add(default_exams[j][0])
        default_courses[i][0].save()
        default_teacher.courses.add(default_courses[i][0])
    default_teacher.save()
    return {
        'user_id' : Teacher.objects.all()[0].id
    }

def course(request, courseNum):
    if request.method == 'GET':
        session = get_session()
        try:
            teacher = Teacher.objects.get(id=session['user_id'])
            course = Course.objects.get(id=courseNum)
        except Course.DoesNotExist:
            #TODO: handle error in the view
            raise Exception("course with specified coursname failed to load")
        context = {
            'teacher': teacher,
            'courseNum': courseNum,
            'course': course.name
            }
        return render(request, 'dashboard/course.html', context)
    elif request.method == 'POST':
        pass

# GET, POST, PUT, DELETE
def course(request, courseNum):
    if request.method == 'GET':
        context = {'teacher': teacher, 'courseNum': courseNum, 'course': cs2050}
        return render(request, 'dashboard/course.html', context)
    elif request.method == 'POST':
        pass

# GET, POST, PUT, DELETE
def exam(request, exam_num):
    pass

# GET
def exam_edit(request, exam_num):
    pass

# GET
def exam_new(request):
    pass

# GET, POST, PUT, DELETE
def exam_question(request, exam_num, question_num):
    pass
