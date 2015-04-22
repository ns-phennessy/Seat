from django.conf.urls import patterns, url
from student import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^take_exam$',views.take_exam)
)
