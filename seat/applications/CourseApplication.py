import logging
from seat.models.course import Course
from seat.models.exam import Exam

logger = logging.getLogger(__name__)

class CourseApplication(object):

    """interactions with courses"""

    def create_exam(self, teacher_query, course_id, name):
        try:
            course = Course.objects.filter(id=course_id, teacher=teacher_query)
            if course.exists():
                new_exam = Exam.objects.create(name=name, course=course.all()[0])
                new_exam.save()
                return [new_exam, "success"]
            return [None, "course did not exist"]
        except Exception, error:
            logger.info("create_exam error:"+str(error))
            raise error
