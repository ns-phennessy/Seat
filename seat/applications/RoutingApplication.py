from django.shortcuts import render, redirect
import datetime
from django.conf import settings

def set_cookie(response, key, value):
        max_age = 60*10 # seconds
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

class RoutingApplication(object):
    """object for abstracting out all those hardcoded urls"""

    def error(self, request, error):
        return render(request, 'dashboard/error.html',{ 'code':500, 'error' : error })

    def invalid_permissions(self, request, msg="Proper authentication required"):
        return render(request, 'dashboard/error.html',{ 'code':401, 'error' : msg })

    def pass_to_login(self, request, msg="Please login first!"):
        request.session['msg'] = msg
        response = redirect('/login/')
        set_cookie(response, 'pass_through', request.build_absolute_uri())
        return response

    def invalid_request(self, request, msg="invalid request"):
        return render(request,'dashboard/error.html',{ 'code':406, 'error' : msg })
    
    def teacher_index(self, request=None):
        """ indicates the default landing page for a teacher upon login """
        return '/dashboard/courses/'

    def student_index(self, request=None):
        """ indicates the default landing page for a student upon login """
        return '/student/'

    def logout(self, request):
        if 'user_id' in request.session:
            print "Logging out user with id", request.session['user_id'] 
        for key in request.session.keys():
            del request.session[key]
        request.session.flush() # force this through the db
        return redirect('/login/')



