# this is the root of all evil
# the goal is to start with a single application that contains
# way more logic than it should, and decompile it into its many
# pieces.
# - Ben

from seat.models.teacher import Teacher
from seat.models.course import Course
from seat.models.exam import Exam, Question, Choice
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
        return "/dashboard/courses/"

    def get_first_course(self, teacher):
        try:
            if teacher.courses.count() == 0:
                return None
            return teacher.courses.all()[0]
        except Exception, error:
            logger.info(str(error))
            raise "failed to get teacher's first course"

    def create_course(self, teacher, name):
        try:
            new_course = Course.objects.create(name=name)
            new_course.save()
            teacher.courses.add(new_course)
            teacher.save()
            return new_course
        except Exception, error:
            logger.warn("failed to add course!:"+str(error))
            raise(error)

    def update_course(self, teacher, course_id, name):
        try:
            Course.objects.update(id=course_id, name=name)
        except Exception, error:
            logger.warn("failed to update course!:"+str(error))
            raise(error)

    def delete_course(self, teacher, course_id):
        try:
            Course.objects.delete(id=course_id)
        except Exception, error:
            logger.warn("failed to delete course!:"+str(error))
            raise(error)

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

    def create_exam(self, course, name):
        try:
            new_exam = Exam.objects.create(name=name)
            new_exam.save()
            course.exams.add(new_exam)
            course.save()
            return new_exam
        except Exception, error:
            logger.info("create_exam error:"+str(error))
            raise error
            return None

class ExamApplication:
    def get_exam_by_id(self, exam_id):
        try:
            exam = Exam.objects.get(id=exam_id)
            return exam

        except Exception, error:
            logger.info("get_exam_by_id error:"+str(error))
            raise error

    def delete_exam(self, exam_id):
        try:
            Exam.objects.delete(id=exam_id)
        except Exception, error:
            logger.warn("failed to delete exam!:"+str(error))
            raise(error)


class QuestionApplication:
    def create_question(self, exam_id, question):
        try:
            category = question['type']
            if category == "multichoice":
                return self.create_multiple_choice_question(exam_id, question)
            else:
                raise Exception("UNSUPPORTED-TYPE, only supports multiple right now.")
        except Exception, error:
            logger.warn("failed to create question in EditExamApplication!: "+str(question))
            raise(error)

    def create_choice(self, choice):
        new_choice = Choice.objects.create(text=choice)
        new_choice.save()
        return new_choice

    def create_multiple_choice_question(self, exam_id, question):
        try:
            answer = self.create_choice(question['options']['answer'])
            text = question['prompt']
            new_question = Question.objects.create(
                text = text,
                answer = answer,
                category = 'multichoice',
                exam = Exam.objects.get(id=exam_id)
                )
            for choice in question['options']['choices']:
                new_choice = self.create_choice(choice)
                new_question.choices.add(new_choice)
            new_question.save()
            return new_question
        except Exception, error:
            logger.warn("failed to create question in QuestionApplication!: "+str(question))
            raise(error)

class ManagingCoursesApplication:
    pass

class GivingExamsApplication:
    pass

class RenderingApplication:
    pass

class RedirectingApplication:
    pass
