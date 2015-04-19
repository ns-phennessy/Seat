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
from django.http import JsonResponse
import json
import logging

logger = logging.getLogger(__name__)

authenticationApplication = AuthenticationApplication()
sessionApplication = SessionApplication()
routingApplication = RoutingApplication()
teacherApplication = TeacherApplication()
courseApplication = CourseApplication()
teacherApplication = TeacherApplication()

def dashboard_index(request):
    try:
        if request.method != 'GET':
            logger.info("non-get request received at dashboard_index endpoint"+str(request))
            return routingApplication.invalid_request(request)

        teacher = teacherApplication.get_teacher_by_id( request.session['user_id'] )
        if not teacher:
            logger.info("user who was not teacher hit dashboard_index:"+str(request))
            sessionApplication.logout(request)
            return routingApplication.invalid_permissions(request)

        # send teacher to go see their courses
        return redirect( teacherApplication.landing_page_url(teacher) )
    except Exception, error:
        logger.error("unhandled error in dashboard_index:"+str(error))
        return routingApplication.error(request, str(error))

def courses(request, course_id):
    try:
        if request.method != 'GET':
            logger.info("courses::non-get request received at courses endpoint"+str(request))
            return routingApplication.invalid_request(request)

        if 'user_id' not in request.session:
            return routingApplication.logout(request)

        teacher = teacherApplication.get_teacher_by_id( request.session['user_id'] )
        if not teacher:
            logger.info("courses::user who was not teacher hit courses endpoint"+str(request))
            sessionApplication.logout(request)
            return routingApplication.invalid_permissions(request)

        course_to_display = None # defining here just to be clear

        if course_id:
            try:
                course_to_display = courseApplication.get_course_by_id(course_id)
            except Exception, error:
                logger.info("courses::courses not found with id "+str(course_id)+" error:"+str(error))
                return redirect( '/dashboard/courses/' )
        else:
            course_to_display = teacherApplication.get_first_course(teacher)

        if course_to_display is not None:
            return render(
                request,
                models.get_course_url(),
                models.get_course_context(teacher, course_id, course_to_display))
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
    #TODO: check user has permissions
    teacher = Teacher.objects.get(id=request.session['user_id'])
    exam = Exam.objects.get(id=exam_num)
    context = { 'teacher': teacher, 'exam': exam , 'question_set_json' : json.dumps(serialize_questions(exam))}
    return render(request, 'dashboard/exam.html', context)

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
