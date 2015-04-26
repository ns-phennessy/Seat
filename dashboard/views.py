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
from seat.applications.TeacherApplication import TeacherApplication
import dashboard.dashboard_view_models as models
from seat.models.course import Course
from seat.models.teacher import Teacher
from seat.models.taken_exam import TakenExam
from django.http import Http404, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
import json
import logging

logger = logging.getLogger(__name__)

authenticationApplication = AuthenticationApplication()
sessionApplication = SessionApplication()
routingApplication = RoutingApplication()
teacherApplication = TeacherApplication()
courseApplication = CourseApplication()
teacherApplication = TeacherApplication()
ID_MAX = 214748364

def id_is_valid(id):
    return (id is not None and str(id).strip() != '' and int(id) < ID_MAX)

def user_is_teacher(user_id):
    if not id_is_valid(user_id):
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
            return routingApplication.pass_to_login(request)

        return redirect(teacherApplication.landing_page_url(teacher))
    except Exception, error:
        logger.error("unhandled error in dashboard_index:"+str(error))
        return routingApplication.error(request, str(error))

def courses(request, course_id):
    try:
        if request.method != 'GET':
            return routingApplication.invalid_request(request, "invalid method")

        is_teacher, teacher = user_is_teacher(request.session.get('user_id'))
        if not is_teacher:
           return routingApplication.pass_to_login(request)

        if not id_is_valid(course_id):
            course_id = None

        course_to_display = None
        
        courses = Course.objects.filter(teacher=teacher)

        if courses.exists():
            if course_id and course_id.strip() != '' and int(course_id):
                course = courses.filter(id=course_id)
                if course.exists():
                    course_to_display = course.all()[0]
            if course_to_display is None:
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
    if request.method != 'GET':
        return routingApplication.invalid_request(request)

    is_teacher, teacher = user_is_teacher(request.session.get('user_id'))
    if not is_teacher:
        return routingApplication.pass_to_login(request)
    
    if not id_is_valid(exam_num):
        return routingApplication.invalid_request(request, "invalid id")

    exam = Exam.objects.filter(id=exam_num, course__teacher = teacher)
    if exam.exists():
        courses = Course.objects.filter(teacher = teacher).all()
        context = { 'teacher': teacher, 'exam': exam.all()[0], 'courses' : courses , 'question_set_json' : json.dumps(serialize_questions(exam.all()[0]))}
        return render(request, 'dashboard/exam.html', context)
    raise Http404("exam not found!")


def render_exam(request, exam_id):
    if request.method != 'GET':
        return routingApplication.invalid_request(request)

    is_teacher, teacher = user_is_teacher(request.session.get('user_id'))
    if not is_teacher:
        return HttpResponseNotAllowed("unauthorized")

    if not id_is_valid(exam_id):
        return HttpResponseBadRequest("exam id invalid")

    exam = Exam.objects.filter(id=exam_id, course__teacher=teacher)

    if not exam.exists():
        return HttpResponseNotFound("exam not found")

    return render(request, 'dashboard/partials/preview-exam.html', { 'exam' : exam.all()[0] })

def render_grades(request, token_id):
    if request.method != 'GET':
        return routingApplication.invalid_permissions(request)

    is_teacher, teacher = user_is_teacher(request.session.get('user_id'))
    if not is_teacher:
        return HttpResponseNotAllowed("unauthorized")

    if not id_is_valid(token_id):
        return HttpResponseBadRequest("Token id is invalid")

    taken_exams = TakenExam.objects.filter(exam__course__teacher=teacher, token__id=token_id)
    total_possible = 0
    if taken_exams.exists():
        exam = taken_exams.all()[0].exam
        questions = exam.question_set.all()
        for question in questions:
            total_possible += question.points
    return render(request, 'dashboard/grades.html', {'taken_exams': taken_exams, 'total_possible':total_possible, 'token_id':token_id})

def render_exam_grading(request, token_id, student_id):
    if request.method != 'GET':
        return routingApplication.invalid_permissions(request,"Only GET requests allowed")

    if not id_is_valid(token_id):
        return routingApplication.invalid_request(request, "Token id is invalid")

    if not id_is_valid(student_id):
        return routingApplication.invalid_request(request, "Student id is invalid")

    is_teacher, teacher = user_is_teacher(request.session.get('user_id'))
    if not is_teacher:
        return routingApplication.invalid_permissions(request, "Not authorized")

    taken_exam_query = TakenExam.objects.filter(student__id = student_id, token__id = token_id)
    if not taken_exam_query.exists():
        raise Http404("Student's exam not found!")

    return render(request, 'dashboard/exam-grading.html', { '' })

