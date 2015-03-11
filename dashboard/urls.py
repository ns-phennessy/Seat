from django.conf.urls import patterns, url
from dashboard import views

urlpatterns = patterns('',
	url(r'^courses/?$', views.dashboard_index),
    url(r'^courses/(\d+)/?$', views.course),
    url(r'^exams/(\d+)/?$', views.exam),
    url(r'^exams/(\d+)/edit/?$', views.exam_edit),
    url(r'^exams/new/?$', views.exam_new),
    url(r'^exams/(\d+)/questions/(\d+)/?$', views.exam_question)
)
