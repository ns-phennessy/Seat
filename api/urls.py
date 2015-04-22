from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
    url(r'course/?$', views.course),
    url(r'exam/?$', views.exam),
    url(r'question/?$', views.question),
    url(r'validate_token/?$', views.validate_token),
    url(r'token/?$', views.token),
    url(r'submission/?$',views.submission),
)
