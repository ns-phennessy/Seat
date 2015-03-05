from django.shortcuts import render, redirect
from dashboard.models import Teacher

def login(request):
    if (request.method == 'GET'):
    	request.session['user_id'] = 1#TODO: actually authenticate
        return render(request, 'login/login.html')
    elif (request.method == 'POST'):
        # assume login successful for now
        # in the future, redirect to teacher's _first_ course, from DB
        return redirect('/dashboard/courses/1')
