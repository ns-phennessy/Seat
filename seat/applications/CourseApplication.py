import logging
from seat.models.course import Course
from seat.models.exam import Exam

logger = logging.getLogger(__name__)

class CourseApplication(object):

    """interactions with courses"""

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
            new_exam = Exam.objects.create(name=name, course=course)
            new_exam.save()
            return new_exam
        except Exception, error:
            logger.info("create_exam error:"+str(error))
            raise error
            return None
