from django.db import models
from django_extensions.db.fields import UUIDField
import uuid

class UUIDModel(models.Model):
	guid = UUIDField(primary_key=False, unique=True, default=uuid.uuid4, editable=False)

class User(UUIDModel):
	# whatever properties all users share
	name = models.TextField() # this is a "Suggestion" since we still have no models
	email = models.EmailField() # sure, why not


class Question(UUIDModel):
	category = models.TextField()
	text = models.TextField()

class Submission(UUIDModel):
	pass#circular reference avoidance

class Exam(UUIDModel):
	name = models.TextField()
	updated_at = models.DateTimeField(auto_now=True)
	questions = models.ManyToManyField(Question)
	def submissions():
		return Submission.objects.get(exam=id)

#circular reference patch
Submission.question = models.OneToOneField(Question)
Submission.exam = models.ForeignKey(Exam)

class Course(UUIDModel):
	name = models.TextField()
	exams = models.ManyToManyField(Exam)

class Teacher(User):
	courses = models.ManyToManyField(Course)