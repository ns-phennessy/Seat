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

logger = logging.getLogger(__name__)


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
