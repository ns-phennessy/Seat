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

# fake teacher data
cs2050 = { 'id': '1', 'name': 'CS2050 - Algorithm Design II' }
ece1210 = { 'id': '2', 'name': 'ECE 1210 - Digital Logic' }
cs1000 = { 'id': '3', 'name': 'CS1000 - Introduction to Computer Science' }
teacher = { 'name': 'Joe Teach', 'courses': [cs2050, ece1210, cs1000] }

def course(request, courseNum):
    if request.method == 'GET':
        context = { 'teacher': teacher,
                    'courseNum': courseNum
                  }
        return render(request, 'teacher/course.html', context)
    elif request.method == 'POST':
        pass
