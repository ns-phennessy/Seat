import logging
from seat.models.student import Student
from seat.models.taken_exam import TakenExam
logger = logging.getLogger(__name__)

class StudentApplication(object):

    """core functionality for interacting with Student entities, abstracts away our models"""

    def get_released_past_exams(self, student):
        try:
            return TakenExam.objects.filter(student=student, completed=True, token__released=True)
        except Exception as error:
            logger.info(str(error))
            raise Exception(error)

    def landing_page_url(self, Student):
        return "/student/"