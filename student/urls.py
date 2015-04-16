from django.conf.urls import patterns, include, url
from django.shortcuts import redirect
from student import views
urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^take_exam$',views.take_exam)
)
