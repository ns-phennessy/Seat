from django.shortcuts import render, redirect

def login(request):
    if (request.method == 'GET'):
        return render(request, 'login/login.html')
    elif (request.method == 'POST'):
        # assume login successful for now
        # in the future, redirect to teacher's _first_ course, from DB
        return redirect('/dashboard/courses/1')
