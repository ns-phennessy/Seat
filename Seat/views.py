from django.http import HttpResponse
from django.template import RequestContext, loader

def login(request):
	return HttpResponse(
		loader.get_template('login.html')
			.render(RequestContext(request)))