from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import redirect

# obliterates user session
def logout(request):
	if request.session['user']:
		print "Logging user out", request.session['user'] 
	for key in request.session.keys():
		del request.session[key]
	request.session.flush() # force this through the db
	return redirect('/login/')

urlpatterns = patterns('',
    url(r'^$', lambda request: redirect('/login/')),
    url(r'^logout/$', logout),
    url(r'^login/', include('login.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include('dashboard.urls')),
)
