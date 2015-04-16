from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import redirect
from seat.applications.RoutingApplication import RoutingApplication

routingApplication = RoutingApplication()

urlpatterns = patterns('',
    url(r'^$', lambda request: redirect('/login/')),
    url(r'^logout/$', routingApplication.logout),
    url(r'^login/', include('login.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^student/',include('student.urls'))
)
