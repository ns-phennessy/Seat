from django.db import models
from seat.models.exam import Exam

class Token(models.Model):
    """key to taking an exam"""
    exam = models.ForeignKey(Exam)
    open = models.BooleanField(default=False)
    released = models.BooleanField(default=False)