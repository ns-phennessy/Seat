import logging
from seat.models.course import Course
from seat.models.exam import Exam

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
            new_exam = Exam.objects.create(name=name)
            new_exam.save()
            course.exams.add(new_exam)
            course.save()
            return new_exam
        except Exception, error:
            logger.info("create_exam error:"+str(error))
            raise error
            return None