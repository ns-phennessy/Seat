from django.db import models
from seat.models.exam import Exam
from seat.models.student import Student
from seat.models.token import Token

class TakenExam(models.Model):
    """represents the root of a submission for an exam"""

    exam = models.ForeignKey(Exam)
    student = models.ForeignKey(Student)
    completed = models.BooleanField(default=False)
    token = models.ForeignKey(Token)
    score = models.DecimalField(decimal_places=2, max_digits = 10)


