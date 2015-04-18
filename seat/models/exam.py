from django.db import models
from seat.models.course import Course

class Exam(models.Model):
    name = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course)
    
class Choice(models.Model):
    text = models.TextField()

class Question(models.Model):
    text = models.TextField()
    category = models.TextField()
    number = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
    choices = models.ManyToManyField(Choice, related_name='question_choices')
    answer = models.ForeignKey(Choice, related_name='question_answer', null=True)
    exam = models.ForeignKey(Exam)
