# this is the root of all evil
# the goal is to start with a single application that contains
# way more logic than it should, and decompile it into its many
# pieces.
# - Ben

from seat.models.teacher import Teacher
from django.conf import settings
from seat.helpers import string_things
import logging
import ldap

# handles no errors, and errors are thrown when
# auth fails so
# if something happens that is unexpected it WILL
# throw an error, so wrap calls to this class in
# try-catch logic. this can't be beaten since its
# how the ldap library wants to work as far as can
# be easily seen (python-ldap module)
logger = logging.getLogger(__name__)

class AuthenticatingApplication:
	
	def connect_to_ldap_server(self):
		logger.debug("connecting to LDAP server host", settings.LDAP_HOST)
		conn = ldap.initialize(settings.LDAP_HOST)
		return conn
	
	def search_for_user(self, username, attributes, conn):
		filter = ('(cn=%s*)' % username)
		logger.debug("searching for user with filter:", filter)
		result_user_list = conn.search_s(
			settings.LDAP_ROOT_SEARCH_DN,
			ldap.SCOPE_SUBTREE,
			filter,
			attributes)
		if not result_user_list:
			logger.info("no user found with username", username)
			raise Exception("no users found with given username")
		user_tuple = result_user_list[0] #a user tuple is like this : (dn, { dict of user attributes })
		user_dn = user_tuple[0]
		user_attrs = user_tuple[1]
		return [user_dn, user_attrs]

	def verify_user_credentials_or_throw(self, dn, password, conn):
		conn.simple_bind(dn, password)
		
	def authenticate(
		self,
		username,
		password,
		attributes = [
			settings.LDAP_DISPLAY_NAME_ATTR,
			settings.LDAP_DISPLAY_NAME_ATTR
			]):
		logger.debug("authenticating username", username)
		conn = self.connect_to_ldap_server()
		#dn = distinguishedName = ldap's name for a node
		dn, user_attrs = self.search_for_user(username, attributes, conn)
		self.verify_user_credentials_or_throw(dn, password, conn)
		#TODO: when we get an email back about how ldap is
		# configured, this will change
		user, new_user_created_bool = Teacher.objects.get_or_create(
				email=user_attrs[settings.LDAP_DISPLAY_NAME_ATTR],
				# .translate(None, chars) will remove the chars
				name= user_attrs[settings.LDAP_DISPLAY_NAME_ATTR][0])
		return user





class EditingExamsApplication:
	pass

class ManagingCoursesApplication:
	pass

class GivingExamsApplication:
	pass