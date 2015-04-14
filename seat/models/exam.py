from django.db import models


class Submission(models.Model):
    pass  # circular reference avoidance


class Exam(models.Model):
    name = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def submissions():
        return Submission.objects.get(exam=id)


class Choice(models.Model):
    text = models.TextField()


class Question(models.Model):
    text = models.TextField()
    category = models.TextField()
    choices = models.ManyToManyField(Choice, related_name='question_choices')
    answer = models.ForeignKey(
        Choice,
        related_name='question_answer',
        null=True)
    exam = models.ForeignKey(Exam)

# circular reference patch
Submission.question = models.OneToOneField(Question)
Submission.exam = models.ForeignKey(Exam)
