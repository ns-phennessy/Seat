from django.db import models
from seat.models.course import Course
from seat.models.user import User


class Student(User):
    courses = models.ManyToManyField(Course)
