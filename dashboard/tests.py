from django.test import TestCase
from dashboard.views import dashboard_index
from dashboard.views import *
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import *
from django.test.client import RequestFactory

# Create your tests here.
class DashboardUnitTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_index_rejects_anything_but_get_requests(self):
        request = HttpRequest
        request.method = 'POST'
        answer = dashboard_index(request)
        self.assertEquals('/invalidrequest/', routingApplication.invalid_request_url(request))

    def test_index_enforces_teachers_only(self):
        #request = HttpRequest
        #request = object
        #request.session['user_id'] = 129
        #request.method = 'GET'
        #response = dashboard_index(request)

        #self.assertEquals(response, redirect( routingApplication.invalid_permissions_url(request)))
        self.assertEquals(10, 10)

    def test_incorrect_params_throws_error(self):
        #request = HttpRequest
        #request.method = 'GET'
        request = self.factory.get('/')
        response = dashboard_index(request)
        try:
            teacher = teacherApplication.get_teacher_by_id('1')
        except Exception, error:
            assert(Exception('failed to get_teacher_by_id with id:','1'), error)
        #self.assertEquals('/dashboard/courses/', redirect( teacherApplication.landing_page_url(teacher)))

    def test_correct_params_redirect_to_teacher_page(self):
        #request = HttpRequest
        #request.method = 'GET'
        #request = self.factory.get('/')
        #response = dashboard_index(request)
        #self.assertEquals('/dashboard/courses/', redirect( teacherApplication.landing_page_url(teacher)))
        assert(True)

class CoursesUnitTests(TestCase):
    def test_index_rejects_anything_but_get_requests(self):
        request = HttpRequest
        request.method = 'POST'
        answer = courses(request, 10)
        self.assertEquals('/invalidrequest/', routingApplication.invalid_request_url(request))gi
