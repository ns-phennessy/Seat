from django.shortcuts import render, redirect
from django.conf import settings
from seat.applications.seat_application import AuthenticatingApplication
import ldap
import logging

logger = logging.getLogger('login')


def login(request):
    if (request.method == 'GET'):
        return render(request, 'login/login.html')
    elif (request.method == 'POST'):
        try:
            logger.info('trying to authenticate %s' % request.POST['username'])
            user = AuthenticatingApplication().authenticate(
                username=request.POST['username'],
                password=request.POST['password'])
            request.session['user_id'] = user.id
            # TODO: should this be different if the user is a teacher/student?
            return redirect('/dashboard/courses/')
        except Exception as error:
            print error
            logger.info(
                'Failed to authenticate user due to error: ',
                str(error))
            context = {'error': str(error).capitalize()}
            return render(request, 'login/login.html', context)
