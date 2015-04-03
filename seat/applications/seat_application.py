# this is the root of all evil
# the goal is to start with a single application that contains
# way more logic than it should, and decompile it into its many
# pieces.
# - Ben

from seat.models.teacher import Teacher
from seat.models.course import Course
from django.conf import settings
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

class TeacherApplication:
    def get_teacher_by_id(self, user_id):
        try:
            return Teacher.objects.get(id=user_id)
        except Exception, error:
            log.info(str(error))
            raise "failed to get_teacher_by_id with id:", user_id

    def landing_page_url(self, teacher):
        return '/dashboard/courses/'

    def get_first_course(self, teacher):
        try:
            if teacher.courses.count() == 0:
                return None
            return teacher.courses.all()[0]
        except Exception, error:
            logger.info(str(error))
            raise "failed to get teacher's first course"

class SessionApplication:
    def logout(self, request):
        pass

class RoutingApplication:
    def error_url(self, request):
        return '/500.html' #TODO: delete this when sure this route exists

    def invalid_permissions_url(self, request):
        return '/invalidpermissions/' #TODO

    def invalid_request_url(self, request):
        return '/invalidrequest/' #TODO

class CourseApplication:
    def get_course_by_id(self, course_id):
        try:
            course = Course.objects.get(id=course_id)
            return course
        except Exception, error:
            logger.info("get_course_by_id error:"+str(error))
            raise error
            return None       

class EditingExamsApplication:
    pass

class ManagingCoursesApplication:
    pass

class GivingExamsApplication:
    pass

class RenderingApplication:
    pass

class RedirectingApplication:
    pass