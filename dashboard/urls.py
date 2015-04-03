from django.conf.urls import patterns, url
from dashboard import views
from django.shortcuts import redirect

urlpatterns = patterns('',
	url(r'^/?$', 						views.dashboard_index),
    url(r'^courses/(\d+)?/?$',          views.courses),
    url(r'^courses/new/?$',             views.course_new),
    url(r'^exams/(\d+)/?$',             views.exam),
    url(r'^exams/(\d+)/edit/?$',        views.exam_edit),
    url(r'^exams/new/?$',               views.exam_new),
    url(r'^exams/(\d+)/questions/?$',   views.questions_index),
    url(r'^questions/(\d+)/?$',         views.question)
)
