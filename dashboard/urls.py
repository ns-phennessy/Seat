from django.conf.urls import patterns, url
from dashboard import views

urlpatterns = patterns('',
	url(r'^/?$', views.dashboard_index),
    url(r'^courses/(\d+)?/?$', views.courses),
    url(r'^exams/(\d+)/edit/?$', views.exam_edit),
    url(r'^rendered-exam/(\d+)/?$', views.render_exam),
    url(r'^grades/(\d+)/?', views.render_grades),
    url(r'^grade-exam/(\d+)/(\d+)/?',views.render_exam_grading, name='manual-grade'),
)
