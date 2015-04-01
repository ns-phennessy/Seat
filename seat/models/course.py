from django.db import models
from seat.models.exam import Exam

class Course(models.Model):
	name = models.TextField()
	exams = models.ManyToManyField(Exam)