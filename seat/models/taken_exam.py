from django.db import models
from seat.models.exam import Exam, Question, Choice
from seat.models.student import Student
from seat.models.token import Token
import datetime
class TakenExam(models.Model):
    """represents the root of a submission for an exam"""

    exam = models.ForeignKey(Exam)
    student = models.ForeignKey(Student)
    completed = models.BooleanField(default=False)
    token = models.ForeignKey(Token, related_name='taken_exam_token')
    score = models.DecimalField(decimal_places=2, max_digits = 10)
    timestamp = models.DateTimeField(default=datetime.datetime.now)


class Submission(models.Model):
    question = models.ForeignKey(Question)
    taken_exam = models.ForeignKey(TakenExam, related_name='submission_taken_exam')
    choices = models.ManyToManyField(Choice)
    correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        unique_together = ('taken_exam','question',)