from django.conf.urls import patterns, url
from dashboard import views
from django.shortcuts import redirect

urlpatterns = patterns('',
	url(r'^/?$', 						views.dashboard_index),
    url(r'^courses/(\d+)?/?$',          views.courses),
    url(r'^exams/(\d+)/edit/?$',        views.exam_edit),
    url(r'^exams/(\d+)/questions/?$',   views.questions_index),
)
