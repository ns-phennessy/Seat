import ldap
import logging
from django.conf import settings
from seat.models.teacher import Teacher
from seat.models.student import Student

logger = logging.getLogger(__name__)

class AuthenticationApplication(object):

    """
        handles no errors, errors are thrown when
        auth fails so if something happens that is unexpected
        it WILL throw an error, so wrap calls to this class in
        try-catch logic.
    """

    def connect_to_ldap_server(self):
        logger.debug("connecting to LDAP server host"+str(settings.LDAP_HOST))
        conn = ldap.initialize(settings.LDAP_HOST)

        conn.simple_bind(settings.LDAP_APP_USER, settings.LDAP_APP_PASS)
        
        return conn

    def search_for_user(self, group, username, attributes, conn):
        ldapfilter = (settings.LDAP_FILTER % username)
        logger.debug("searching for user with filter:"+str(ldapfilter))

        try:
            result_user_list = conn.search_s(
                group, # root
                ldap.SCOPE_SUBTREE, # search every tree below root given
                ldapfilter, # something like cn=username
                attributes) # what we want to get back
        except ldap.NO_SUCH_OBJECT as e:
            logger.debug("search root invalid, this is a configuration problem:"+group)
            raise AssertionError("search root invalid, this is a configuration problem")
        else: 
            if not result_user_list:
                return [False,[]]
                
        # a user tuple is like this : (dn, { dict of user attributes })
        user_tuple = result_user_list[0]
        user_dn = user_tuple[0]
        user_attrs = user_tuple[1]
        return [user_dn, user_attrs]

    def verify_user_credentials_or_throw(self, dn, password, conn):
        conn.simple_bind(dn, password)

    def authenticate(
            self,
            username,
            password,
            attributes=[
                settings.LDAP_MAIL_ATTR,# we take the first because its always an array
                settings.LDAP_DISPLAY_NAME_ATTR]):
        logger.debug("authenticating username", username)
        conn = self.connect_to_ldap_server()
        
        # dn = distinguishedName = ldap's name for a node
        # the dn == False if the search fails
        is_student = False

        # is the user a teacher?
        distinguishedName, user_attrs = self.search_for_user(
                                              settings.LDAP_STAFF_SEARCH_DN,
                                              username, attributes, conn)
        # is the user a student?
        if not distinguishedName:
            distinguishedName, user_attrs = self.search_for_user(
                                              settings.LDAP_STUDENT_SEARCH_DN,
                                              username, attributes, conn)
            if distinguishedName:
                is_student = True
            else:
                raise AuthenticationError("User not found")

        try: 
            self.verify_user_credentials_or_throw(distinguishedName, password, conn)
            logger.debug("user attributes:"+str(user_attrs))
        except Exception as error:
            raise AssertionError("Authentication has failed")  
         
        if not is_student:
            teacher, new_user_created = Teacher.objects.get_or_create(
                email = user_attrs[settings.LDAP_MAIL_ATTR][0],
                name = user_attrs[settings.LDAP_DISPLAY_NAME_ATTR][0])
            if new_user_created:
                teacher.save()
            return [teacher, True] # False == is_teacher
        else:
            student, new_user_created = Student.objects.get_or_create(
                email = user_attrs[settings.LDAP_MAIL_ATTR][0],
                name = user_attrs[settings.LDAP_DISPLAY_NAME_ATTR][0])
            if new_user_created:
                student.save()
            return [student, False] # True == is_teacher
