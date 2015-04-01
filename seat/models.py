from django.db import models

class User(models.Model):
	# whatever properties all users share
	name = models.TextField() # this is a "Suggestion" since we still have no models
	email = models.EmailField() # sure, why not


class Question(models.Model):
	category = models.TextField()
	text = models.TextField()

class Submission(models.Model):
	pass#circular reference avoidance

class Exam(models.Model):
	name = models.TextField()
	updated_at = models.DateTimeField(auto_now=True)
	questions = models.ManyToManyField(Question)
	def submissions():
		return Submission.objects.get(exam=id)

#circular reference patch
Submission.question = models.OneToOneField(Question)
Submission.exam = models.ForeignKey(Exam)

class Course(models.Model):
	name = models.TextField()
	exams = models.ManyToManyField(Exam)

class Teacher(User):
	courses = models.ManyToManyField(Course)