import logging
from seat.models.exam import Choice, Question, Exam

logger = logging.getLogger(__name__)

class QuestionApplication(object):

    """complex functionality for dealing with question objects"""

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

    def delete_question(self, question_id):
        try:
            Question.objects.get(id=question_id).delete()
        except Exception, error:
            logger.warn("failed to delete question!:"+str(error))
            raise(error)
