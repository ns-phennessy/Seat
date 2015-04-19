from django.db import models
from seat.models.teacher import Teacher

class Course(models.Model):
    name = models.TextField()
    teacher = models.ForeignKey(Teacher)