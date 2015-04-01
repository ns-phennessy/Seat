from django.shortcuts import render, redirect
from seat.models import Teacher
from django.conf import settings
import ldap

def login(request):
	if (request.method == 'GET'):
		return render(request, 'login/login.html')
	elif (request.method == 'POST'):
		ldap_connection = ldap.initialize(settings.LDAP_HOST)
		username = request.POST['username']
		password = request.POST['password']
		print 'attempted authentication of %s' % username
		try:
			search = '(cn=%s*)' % username

			# match first user with name
			user_result_list = ldap_connection.search_s(
				settings.LDAP_ROOT_SEARCH_DN,
				ldap.SCOPE_SUBTREE,
				search,
				# these are the things we get out of the objects
				['cn','mail','gn','email'])
			user_tuple = user_result_list[0] #a user tuple is like this : (dn, { dict of user attributes })
			user_dn = user_tuple[0]

			# this line throws an error if the user's password is incorrect
			ldap_connection.simple_bind(user_dn, password) 

			user_attrs = user_tuple[1]

			# currently making the strong assumption that the givenName is the full user display name
			# create or find the user with the matching email + name
			user, new_user_created_bool = Teacher.objects.get_or_create(
				email=user_attrs['mail'], name=user_attrs['givenName'])

			# finally, put the user_id in the session so we can get the user back later, 
			# the user is now authenticated, assuming our sessions are not spoofed	
			request.session['user_id'] = user.id

			#TODO: should this be different if the user is a teacher/student?
			return redirect('/dashboard/courses/')
		except Exception, error:
			print 'failed to authenticate user due to error: ', error
			return redirect('/login?message=failed+to+authenticate')
