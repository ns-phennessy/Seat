from django.contrib import admin

from seat.models.user import User
from seat.models.exam import Question, Submission, Exam, Choice
from seat.models.course import Course
from seat.models.teacher import Teacher

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Exam)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Choice)
