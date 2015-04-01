from django.db import models

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