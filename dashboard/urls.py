from django.conf.urls import patterns, url
from teacher import views

urlpatterns = patterns('',
    url(r'^courses/(\d+)/$', views.course)
)
