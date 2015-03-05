from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import redirect

urlpatterns = patterns('',
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^login/', include('login.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^$', lambda request: redirect('/login/'))
)
