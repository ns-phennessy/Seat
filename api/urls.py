from django.conf.urls import patterns, include, url
from django.shortcuts import redirect
from api import views
urlpatterns = patterns('',
    url(r'course/?$', views.course),
    url(r'exam/?$', views.exam),
    url(r'question/?$', views.question)
)
