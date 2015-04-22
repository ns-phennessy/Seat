import logging
from seat.models.course import Course

logger = logging.getLogger(__name__)

class TeacherApplication(object):

    """core functionality for interacting with teacher entities, abstracts away our models"""

    def landing_page_url(self, teacher):
        return "/dashboard/courses/"

    def get_first_course(self, teacher):
        courses = Course.objects.filter(teacher=teacher)
        if courses.exists():
            return courses.all()[0]
        else:
            return None

    def create_course(self, teacher, name):
        try:
            new_course = Course.objects.create(name=name, teacher=teacher)
            new_course.save()
            return [new_course, "success"]
        except Exception, error:
            logger.warn("failed to add course!:"+str(error))
            raise Exception(error)

    def update_course(self, teacher, course_id, name):
        try:
            course = Course.objects.filter(id=course_id, teacher=teacher)
            if course.exists():
                course = course.all()[0];
                course.name = name
                course.save()
                return [True, "success"]
            return [False, "course did not exist"]
        except Exception, error:
            logger.warn("failed to update course!:"+str(error))
            raise Exception(error)

    def delete_course(self, teacher, course_id):
        try:
            course = Course.objects.filter(id=course_id, teacher=teacher)
            if course.exists():
                course.delete()
                return [True, "success"]
            else:
                return [False, "course did not exist"]
        except Exception, error:
            logger.warn("failed to delete course!:"+str(error))
            raise Exception(error)