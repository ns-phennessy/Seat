import logging
from seat.models.exam import Choice, Question, Exam

logger = logging.getLogger("applications")

class QuestionApplication(object):

    """complex functionality for dealing with question objects"""

    def upsert_question(self, exam_id, question):
        try:
            category = question['type']
            if category == "multichoice":
                return self.upsert_multiple_choice_question(exam_id, question)
            elif category == "truefalse":
                return self.upsert_true_false_question(exam_id, question)
            elif category == "shortanswer":
                return self.upsert_short_answer_question(exam_id, question)
            elif category == "essay":
                return self.upsert_essay_question(exam_id, question)
            else:
                raise Exception("UNSUPPORTED-TYPE, only supports multiple right now.")
        except Exception, error:
            logger.warn("failed to upsert question in EditExamApplication!: "+str(question))
            raise(error)

    def create_choice(self, text):
        new_choice = Choice.objects.create(text=text)
        new_choice.save()
        return new_choice

    def upsert_multiple_choice_question(self, exam_id, question_json):
        try:
            if 'question_id' in question_json: # update
                question = Qestion.objects.get(id=question_json['question_id'])
                question.text = question_json['prompt']
                question.answer.text = question_json['options']['answer']
                for choice in question.choices.all():
                    choice.delete()
            else: #insert
                answer = self.create_choice(question_json['options']['answer'])
                text = question_json['prompt']
                question = Question.objects.create(
                    text = text,
                    answer = answer,
                    category = 'multichoice',
                    exam = Exam.objects.get(id=exam_id)
                    )
            # both
            for choice in question_json['options']['choices']:
                new_choice = self.create_choice(choice)
                question.choices.add(new_choice)

            # complete
            question.save()
            return question
        except Exception, error:
            logger.warn("failed to upsert question in QuestionApplication!: "+str(question_json))
            raise(error)

    def upsert_short_answer_question(self, exam_id, question_json):
        try:
            if 'question_id' in question_json and question_json['question_id'].strip() != '':
                questions = Question.objects.filter(id=question_json['question_id'])
                if not questions.exists():
                    return [False, "question does not exist"]
                question = questions.all()[0]
                question.text = question_json['prompt']
                question.points = int(question_json['points'] if question_json['points'].strip() != '' else 0)
                question.number = int(question_json['number'] if question_json['number'].strip() != '' else 0)
            else:
                text = question_json['prompt']
                question = Question.objects.create(
                    number = int(question_json['number'] if question_json['number'].strip() != '' else 0),
                    points = int(question_json['points'] if question_json['points'].strip() != '' else 0),
                    text = text,
                    category = 'shortanswer',
                    exam = Exam.objects.get(id=exam_id))

            question.save()
            return [question, 'success']
        except Exception as error:
            logger.warn(str(error))
            raise(error)

    def upsert_essay_question(self, exam_id, question):
        try:
            if 'question_id' in question_json:
                question = Question.objects.get(id=question_json['question_id'])
                question.text = question_json['prompt']
            else:
                text = question_json['prompt']
                question = Question.objects.create(
                    text = text,
                    category = 'essay',
                    exam = Exam.objects.get(id=exam_id))

            question.save()
            return question
        except Exception as error:
            logger.debug(str(error))
            raise(error)

    def upsert_true_false_question(self, exam_id, question_json):
        try:
            if 'question_id' in question_json:
                question.text = question_json['prompt']
                question.answer.text = question_json['options']['answer']
            else:
                text = question_json['prompt']
                answer = self.create_choice(text=question_json['options']['answer'])
                new_question = Question.objects.create(
                    text = text,
                    answer = answer,
                    category = 'truefalse',
                    exam = Exam.objects.get(id=exam_id)
                    )
                true_choice = self.create_choice(text="true")
                false_choice = self.create_choice(text="false")
                new_question.choices.add(true_choice)
                new_question.choices.add(false_choice)
            new_question.save()
            return new_question
        except Exception as error:
            logger.debug(str(error))
            raise(error)

    def delete_question(self, question_id):
        try:
            questions = Question.objects.filter(id=question_id)
            if questions.exists():
                questions.delete()
                return [True, "success"]
            else:
                return [False, "Question did not exist"]
        except Exception, error:
            logger.warn("failed to delete question!:"+str(error))
            raise(error)
