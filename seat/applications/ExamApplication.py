import logging
from seat.models.exam import Exam

logger = logging.getLogger(__name__)

class ExamApplication(object):

    """description of class"""

    def get_exam_by_id(self, exam_id):
        try:
            exam = Exam.objects.get(id=exam_id)
            return exam

        except Exception, error:
            logger.info("get_exam_by_id error:"+str(error))
            raise error

    def delete_exam(self, exam_id):
        try:
            Exam.objects.get(id=exam_id).delete()
        except Exception, error:
            logger.warn("failed to delete exam!:"+str(error))
            raise(error)
