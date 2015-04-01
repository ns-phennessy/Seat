from django.shortcuts import render
from django.conf import settings
from django.core import serializers

class DashboardExceptionMiddleware(object):
	def process_exception(self, request, exception):
		if not settings.DEBUG:
			return render(request, 'dashboard/404.html')
		else:
			print request, exception
			return request