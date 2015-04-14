#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import date
from seat.models.teacher import Teacher
from seat.models.exam import Question, Submission, Exam
from seat.applications.seat_application import AuthenticatingApplication
from seat.applications.seat_application import SessionApplication
from seat.applications.seat_application import TeacherApplication
from seat.applications.seat_application import RoutingApplication
from seat.applications.seat_application import CourseApplication
from dashboard import dashboard_view_models
from seat.models.course import Course
from django.http import JsonResponse
import logging
logging.basicConfig()

logger = logging.getLogger('dashboard')

authenticationApplication = AuthenticatingApplication()
sessionApplication = SessionApplication()
routingApplication = RoutingApplication()
teacherApplication = TeacherApplication()
courseApplication = CourseApplication()


def dashboard_index(request):
    try:
        if request.method != 'GET':
            logger.info(
                "non-get request received at dashboard_index endpoint" +
                str(request))
            return redirect(routingApplication.invalid_request_url(request))

        teacher = teacherApplication.get_teacher_by_id(
            request.session['user_id'])
        if not teacher:
            logger.info(
                "user who was not teacher hit dashboard_index:" +
                str(request))
            sessionApplication.logout(request)
            return redirect(
                routingApplication.invalid_permissions_url(request))

        # send teacher to go see their courses
        return redirect(teacherApplication.landing_page_url(teacher))
    except Exception as error:
        logger.error("unhandled error in dashboard_index:" + str(error))
        return redirect(routingApplication.error_url(request))


def courses(request, course_id):
    try:
        if request.method != 'GET':
            logger.info(
                "courses::non-get request received at courses endpoint" +
                str(request))
            return redirect(routingApplication.invalid_request_url(request))

        teacher = teacherApplication.get_teacher_by_id(
            request.session['user_id'])
        if not teacher:
            logger.info(
                "courses::user who was not teacher hit courses endpoint" +
                str(request))
            sessionApplication.logout(request)
            return redirect(
                routingApplication.invalid_permissions_url(request))

        course_to_display = None  # defining here just to be clear

        if course_id:
            try:
                course_to_display = courseApplication.get_course_by_id(
                    course_id)
            except Exception as error:
                logger.info(
                    "courses::courses not found with id " +
                    str(course_id) +
                    " error:" +
                    str(error))
                return redirect('/dashboard/courses/')
        else:
            course_to_display = teacherApplication.get_first_course(teacher)

        if course_to_display is not None:
            return render(
                request,
                dashboard_view_models.get_course_url(),
                dashboard_view_models.get_course_context(teacher, course_id, course_to_display))
        else:
            return render(
                request,
                dashboard_view_models.get_nocourse_url(),
                dashboard_view_models.get_nocourse_context(teacher))

    except Exception as error:
        logger.error("courses::unhandled error:" + str(error))
        return redirect(routingApplication.error_url(request))

# POST


def course_new(request):
    # TODO: check user has permissions
    if request.method == 'POST':
        try:
            new_course = Course.objects.create(name=request.POST['name'])
            teacher = Teacher.objects.get(id=request.session['user_id'])
            new_course.save()
            teacher.courses.add(new_course)
            teacher.save()
            return JsonResponse(
                {'success': True, 'error': False, 'id': str(new_course.id)})
        except Exception as e:
            # TODO: handle error case properly, still haven't hit enough of
            # these to decide yet how
            print e
            return JsonResponse(
                {'success': False, 'error': True, 'message': str(e)})
    # TODO: handle else condition

# GET?, POST, PUT, DELETE


def exam(request, exam_num):
    # TODO: check user has permissions
    exam = Exam.objects.get(id=exam_num)
    if request.method == 'DELETE':
        exam.delete()
        return JsonResponse({'success': True, 'error': False})
    # TODO: handle other methods

# GET


def exam_edit(request, exam_num):
    # TODO: check user has permissions
    teacher = Teacher.objects.get(id=request.session['user_id'])
    exam = Exam.objects.get(id=exam_num)
    context = {'teacher': teacher, 'exam': exam}
    return render(request, 'dashboard/exam.html', context)

# GET


def exam_new(request):
    # TODO: check user has permissions
    if request.method == 'GET':
        teacher = Teacher.objects.get(id=request.session['user_id'])
        context = {'teacher': teacher}
        return render(request, 'dashboard/exam.html', context)
    # TODO: handle else condition

question_urls = {'Multiple Choice': 'dashboard/multiple-choice.html', 'True/False': 'dashboard/true-false.html', 'Short Answer': 'dashboard/short-answer.html', 'Essay': ''
                 }

# GET


def questions_index(request, exam_id):
    if request.method == 'GET':
        exam = Exam.objects.get(id=exam_id)
        context = {'exam': exam}
        return render(request, 'dashboard/questions.html', context)

# GET, POST, PUT, DELETE


def question(request, question_id):
    # TODO: check user has permissions
    question = Question.objects.get(id=question_id)
    if request.method == 'GET':
        context = {'question': question}
        return render(request, question_urls[question.category], context)
    elif request.method == 'DELETE':
        question.delete()
        return JsonResponse({'success': True, 'error': False})
