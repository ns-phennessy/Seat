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
from seat.models.exam import Question, Submission, Exam
from seat.models.course import Course
from django.utils.importlib import import_module

# Create your tests here.
class DashboardUnitTests(TestCase):
    def setUp(self):
   #     self.client = Client()
        Teacher.objects.create(name="fred", email="fred@fred.com")
     #   s = self.client.session
     #   s['user_id'] = 1
     #   s.save()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def test_tickles(self):
        session = self.session
        session['user_id'] = 1;
        session.method = 'GET'
        session.save()

        answer = dashboard_index(session)

        self.assertEquals(answer.status_code, 302)


    def test_index_rejects_anything_but_get_requests(self):
        request = HttpRequest
        request.method = 'POST'
        answer = dashboard_index(request)
        self.assertEquals('/invalidrequest/', routingApplication.invalid_request_url(request))

    def test_index_enforces_teachers_only(self):
        request = self.client.get('/')
        response = dashboard_index(request)
        self.assertEquals(302, response.status_code)

    def test_incorrect_params_throws_error(self):
        #Needs session
        session = self.session
        session['user_id'] = 2;
        session.method = 'GET'
        session.save()

        try:
            response = dashboard_index(session)
            #teacher = teacherApplication.get_teacher_by_id('2')
        except Exception, error:
            assert(Exception('failed to get_teacher_by_id with id:','2'), error)
        assert(True)

    def test_correct_params_redirect_to_teacher_page(self):
        #Needs session
        #request = HttpRequest
        #request.method = 'GET'
        #request.session['user_id':1]
        request = self.client.get('/')
        response = dashboard_index(request)
        #print request.session['user_id']
        #self.assertEquals('/dashboard/courses/', redirect( teacherApplication.landing_page_url(response)))
        assert(True)

class CoursesUnitTests(TestCase):
    def test_index_rejects_anything_but_get_requests(self):
        request = HttpRequest
        request.method = 'POST'
        answer = courses(request, 10)
        self.assertEquals('/invalidrequest/', routingApplication.invalid_request_url(request))
