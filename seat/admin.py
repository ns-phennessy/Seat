from django.contrib import admin

from seat.models.user import User
from seat.models.exam import Question, Exam, Choice
from seat.models.course import Course
from seat.models.teacher import Teacher
from seat.models.student import Student
from seat.models.taken_exam import TakenExam, Submission
from seat.models.token import Token

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Exam)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Choice)
admin.site.register(Token)
admin.site.register(TakenExam)
