from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate

def login(request):
	if (request.method == 'GET'):
		return render(request, 'login.html')
	if (request.method == 'POST'):
		print request.POST
		return render(request, 'login.html')