from django.conf.urls import patterns, url
from dashboard import views
from django.shortcuts import redirect

urlpatterns = patterns('',
	url(r'^/?$', lambda req: redirect('courses/')),
	url(r'^courses/?$',                 views.dashboard_index),
    url(r'^courses/(\d+)/?$',           views.course),
    url(r'^courses/new/?$',             views.course_new),
    url(r'^exams/?$',                   views.exam_index),
    url(r'^exams/(\d+)/?$',             views.exam),
    url(r'^exams/(\d+)/edit/?$',        views.exam_edit),
    url(r'^exams/new/?$',               views.exam_new),
    url(r'^exams/(\d+)/questions/?$',   views.questions_index),
    url(r'^questions/(\d+)/?$',         views.question)
)
