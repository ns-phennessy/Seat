#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from seat.models.teacher import Teacher
from seat.models.exam import Exam
from seat.applications.SessionApplication import SessionApplication
from seat.applications.RoutingApplication import RoutingApplication
from seat.applications.CourseApplication import CourseApplication
from seat.applications.AuthenticationApplication import AuthenticationApplication
from seat.applications.ExamApplication import ExamApplication
from seat.applications.TeacherApplication import TeacherApplication
import seat.applications.CourseApplication
import dashboard.dashboard_view_models as models
from seat.models.course import Course
from seat.models.teacher import Teacher
from django.http import JsonResponse, Http404
import json
import logging

logger = logging.getLogger(__name__)

authenticationApplication = AuthenticationApplication()
sessionApplication = SessionApplication()
routingApplication = RoutingApplication()
teacherApplication = TeacherApplication()
courseApplication = CourseApplication()
teacherApplication = TeacherApplication()

def user_is_teacher(user_id):
    if user_id is None or user_id == '':
        return [False, None]
    teacher = Teacher.objects.filter(id=user_id)
    if teacher.exists():
        return [True, teacher.all()[0]]
    return [False, None]

def dashboard_index(request):
    try:
        if request.method != 'GET':
            return routingApplication.invalid_request(request)

        is_teacher, teacher = user_is_teacher(request.session.get('user_id'))
        if not is_teacher:
            return routingApplication.invalid_permissions(request,"you are not a teacher")

        return redirect(teacherApplication.landing_page_url(teacher))
    except Exception, error:
        logger.error("unhandled error in dashboard_index:"+str(error))
        return routingApplication.error(request, str(error))

def courses(request, course_id):
    try:
        if request.method != 'GET':
            return routingApplication.invalid_request(request)

        is_teacher, teacher = user_is_teacher(request.session.get('user_id'))
        if not is_teacher:
            return routingApplication.invalid_permissions(request, "you are not a teacher")

        course_to_display = None
        courses = Course.objects.filter(teacher=teacher)

        if course_id and courses.exists():
            course = courses.filter(id=course_id)
            if course.exists():
                course_to_display = course.all()[0]
        elif courses.exists():
            course_to_display = courses.all()[0]

        if course_to_display is not None:
            return render(
                request,
                models.get_course_url(),
                models.get_course_context(teacher, course_id, course_to_display, courses.all()))
        else:
            return render(
                request,
                models.get_nocourse_url(),
                models.get_nocourse_context(teacher))

    except Exception as error:
        logger.error("courses::unhandled error:"+str(error))
        return routingApplication.error(request, str(error))

def serialize_questions(exam):
    questions = []
    for question in exam.question_set.all():
        questions.append(question.prep_for_serialization())
    return questions;

# GET
def exam_edit(request, exam_num):
    teacher = Teacher.objects.filter(id=request.session['user_id'])
    exam = Exam.objects.filter(id=exam_num, course__teacher= teacher)
    if teacher.exists() and  exam.exists():
        courses = Course.objects.filter(teacher = teacher).all()
        context = { 'teacher': teacher, 'exam': exam, 'courses' : courses , 'question_set_json' : json.dumps(serialize_questions(exam.all()[0]))}
        return render(request, 'dashboard/exam.html', context)
    else:
        return routingApplication.invalid_permissions(request)

question_urls = { 'Multiple Choice': 'dashboard/multiple-choice.html'
                , 'True/False': 'dashboard/true-false.html'
                , 'Short Answer': 'dashboard/short-answer.html'
                , 'Essay': ''
                }
def questions_index(request, exam_id):
    if request.method == 'GET':
        exam = Exam.objects.get(id=exam_id)
        context = { 'exam': exam }
        return render(request, 'dashboard/questions.html', context)
