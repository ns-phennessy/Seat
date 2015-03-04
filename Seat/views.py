from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

def login(request):
    if (request.method == 'GET'):
        return render(request, 'login.html')
    elif (request.method == 'POST'):
        # assume login successful for now
        # in the future, redirect to teacher's _first_ course, from DB
        return redirect('/courses/1')

def course(request, courseNum):
    if request.method == 'GET':
        return render(request, 'teacher/course.html')
    elif request.method == 'POST':
        pass
