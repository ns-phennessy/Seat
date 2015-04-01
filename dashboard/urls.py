from django.conf.urls import patterns, url
from dashboard import views
from django.shortcuts import redirect
from seat.route_right_guards import teacher,student

urlpatterns = patterns('',
	url(r'^/?$', lambda req: redirect('courses/')),
	url(r'^courses/?$',                 teacher(views.dashboard_index)),
    url(r'^courses/(\d+)/?$',           teacher(views.course)),
    url(r'^courses/new/?$',             teacher(views.course_new)),
    url(r'^exams/?$',                   teacher(views.exam_index)),
    url(r'^exams/(\d+)/?$',             teacher(views.exam)),
    url(r'^exams/(\d+)/edit/?$',        teacher(views.exam_edit)),
    url(r'^exams/new/?$', views.exam_new),
    url(r'^exams/(\d+)/questions/?$',   teacher(views.questions_index)),
    url(r'^questions/(\d+)/?$',         teacher(views.question))
)
