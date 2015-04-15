import logging
from seat.models.teacher import Teacher
from seat.models.course import Course

logger = logging.getLogger(__name__)

class TeacherApplication(object):

    """core functionality for interacting with teacher entities, abstracts away our models"""

    def get_teacher_by_id(self, user_id):
        try:
            return Teacher.objects.get(id=user_id)
        except Exception, error:
            logger.info(str(error))
            raise Exception( "failed to get_teacher_by_id with id:", user_id )

    def landing_page_url(self, teacher):
        return "/dashboard/courses/"

    def get_first_course(self, teacher):
        try:
            if teacher.courses.count() == 0:
                return None
            return teacher.courses.all()[0]
        except Exception, error:
            logger.info(str(error))
            raise Exception( "failed to get teacher's first course" )

    def create_course(self, teacher, name):
        try:
            new_course = Course.objects.create(name=name)
            new_course.save()
            teacher.courses.add(new_course)
            teacher.save()
            return new_course
        except Exception, error:
            logger.warn("failed to add course!:"+str(error))
            raise Exception(error)

    def update_course(self, teacher, course_id, name):
        try:
            course = Course.objects.get(id=course_id)
            course.name = name
            course.save()
        except Exception, error:
            logger.warn("failed to update course!:"+str(error))
            raise Exception(error)

    def delete_course(self, teacher, course_id):
        try:
            Course.objects.get(id=course_id).delete()
        except Exception, error:
            logger.warn("failed to delete course!:"+str(error))
            raise Exception(error)