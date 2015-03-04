from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^login/', include('login.urls')),
    url(r'^dashboard/', include('teacher.urls'))
)
