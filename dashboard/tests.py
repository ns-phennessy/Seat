from django.test import TestCase
from django.conf import settings
from dashboard.views import dashboard_index
from dashboard.views import *
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import *
from django.test.client import RequestFactory
from django.test import Client
from seat.models.teacher import Teacher
from seat.models.exam import Question, Exam
from seat.models.course import Course
from django.utils.importlib import import_module

# Create your tests here.
class DashboardUnitTests(TestCase):
    def setUp(self):
        self.client = Client()
        Teacher.objects.create(name="fred", email="fred@fred.com")

        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def test_index_rejects_anything_but_get_requests(self):
        request = HttpRequest
        request.method = 'POST'
        answer = dashboard_index(request)

        self.assertContains(answer, "invalid request")

    def test_index_enforces_teachers_only(self):
        s = self.client.session
        s['user_id'] = '2'
        s.save()
        response = self.client.get('/dashboard/')

        self.assertContains(response, 'not a teacher')

    def test_correct_params_redirect_to_teacher_page(self):
        s = self.client.session
        s['user_id'] = '1'
        s.save()
        response = self.client.get('/dashboard/')

        self.assertEquals('http://testserver/dashboard/courses/', response.url)

class CoursesUnitTests(TestCase):
    def setUp(self):
        self.client = Client()
        Teacher.objects.create(name="fred", email="fred@fred.com")

        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def test_course_rejects_anything_but_get_requests(self):
        request = HttpRequest
        request.method = 'POST'
        answer = courses(request, 10)

        self.assertContains(answer, "invalid method")

    def test_courses_displays_no_courses_if_none_are_made(self):
        s = self.client.session
        s['user_id'] = '1'
        s.save()
        response = self.client.get('/dashboard/courses/')

        self.assertContains(response, 'without a course')

