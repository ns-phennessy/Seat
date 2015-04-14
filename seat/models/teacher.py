from django.db import models
from seat.models.user import User
from seat.models.course import Course


class Teacher(User):
    courses = models.ManyToManyField(Course)
