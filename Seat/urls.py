from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import redirect

def redirect_to_login(request):
	return redirect('/login/')

urlpatterns = patterns('',
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^login/', include('login.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'$', redirect_to_login)
)
