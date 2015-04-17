from django.http import Http404
from django.shortcuts import render, redirect

class RoutingApplication(object):
    """object for abstracting out all those hardcoded urls"""

    def error(self, request, error):
        return render('error.html',{ 'code':500, 'error' : error })

    def invalid_permissions(self, request, msg="proper authentication required"):
        return render('error.html',{ 'code':401, 'error' : msg })

    def invalid_request(self, request):
        return render('error.html',{ 'code':406, 'error' : "not acceptable" })
    
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



