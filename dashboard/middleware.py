from django.shortcuts import render

class DashboardExceptionMiddleware(object):
    def process_exception(self, request, exception):
		return render(request, 'dashboard/404.html')