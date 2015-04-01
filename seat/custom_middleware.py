from django.shortcuts import render

class DashboardExceptionMiddleware(object):
	def process_exception(self, request, exception):
		if settings.DEBUG:
			return render(request, 'dashboard/404.html')
		else:
			return request