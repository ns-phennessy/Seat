from seat.applications.QuestionApplication import QuestionApplication
from seat.applications.TokenApplication import TokenApplication
from seat.models.taken_exam import TakenExam, Submission
from seat.models.exam import Question, Choice
from django.http import JsonResponse, HttpResponseServerError, HttpResponseNotAllowed, HttpResponseForbidden
from api.helpers import endpoint_checks
import json
import logging

logger = logging.getLogger('api')

questionApplication = QuestionApplication()
tokenApplication = TokenApplication()

# POST
def upsert_success_json_model():
    return JsonResponse({
        'success': True,
        'error': False
    })

def submission_logic(student, request):
    try:
        #TODO: be sure sessions don't expire real fast
        token = tokenApplication.is_valid(request.session['token']) # placed during validation
        if not token:
            return HttpResponseNotAllowed("invalid token")

        submission_json = json.loads(request.POST['submission'])

        # it is important that all of these properties are satisfied
        taken_exam,new_taken = TakenExam.objects.get_or_create(exam=token.exam, student=student, completed=False, token=token, score=0)
        
        if new_taken:
            taken_exam.save()
        
        question = Question.objects.filter(id=submission_json['question_id'])
        if question.count() == 0:
            return HttpResponseNotAllowed("this question is not for this token/exam")
        else:
            question = question.all()[0]

        submission,new_sub = Submission.objects.get_or_create(question=question, taken_exam=taken_exam)
        
        if new_sub:
            submission.save()

        if question.category == 'shortanswer':
            if not submission.choices.exists():
                choice = Choice.objects.create(text = submission_json['text'])
                choice.save()
                submission.choices.add(choice)
            else:
                choice = submission.choices.all()[0]
                choice.text = submission_json['text']
                choice.save()
        else:
            return HttpResponseForbidden("unsupported")
        
        submission.save()
        return upsert_success_json_model()
    except Exception as error:
        logger.info(str(error))
        return HttpResponseServerError("server error")

def submit(request):
    return endpoint_checks.standard_student_endpoint(
        "submission",
        ['submission'],
        'POST',
        request,
        submission_logic)
