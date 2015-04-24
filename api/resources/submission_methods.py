from seat.applications.QuestionApplication import QuestionApplication
from seat.applications.TokenApplication import TokenApplication
from seat.models.taken_exam import TakenExam, Submission
from seat.models.exam import Question, Choice
from django.http import JsonResponse, HttpResponseServerError, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
from api.helpers import endpoint_checks
import json
import logging

logger = logging.getLogger('api')

questionApplication = QuestionApplication()
tokenApplication = TokenApplication()

# POST
def upsert_success_json_model(id):
    return JsonResponse({
        'success': True,
        'error': False,
        'id': id
    })

def submission_logic(student_query, request):
    try:
        #TODO: be sure sessions don't expire real fast
        token = tokenApplication.is_valid(request.session['token']) # placed during validation
        if not token:
            return HttpResponseNotAllowed("invalid token")

        submission_json = json.loads(request.POST['submission'])

        if 'choices' not in submission_json:
            return HttpResponseBadRequest("no choices");

        if 'question_id' not in submission_json:
            return HttpResponseBadRequest("no question id!")

        if not endpoint_checks.id_is_valid(submission_json.get('question_id')):
            return HttpResponseBadRequest("bad question_id")

        # it is important that all of these properties are satisfied
        taken_exam,new_taken = TakenExam.objects.get_or_create(exam=token.exam, student=student_query.all()[0], completed=False, token=token, score=0)
        
        if new_taken:
            taken_exam.save()
        
        question = Question.objects.filter(id=submission_json['question_id'], exam=token.exam)
        if question.count() == 0:
            return HttpResponseNotAllowed("this question is not for this token/exam")
        
        question = question.all()[0]

        submission_query = Submission.objects.filter(question=question, taken_exam__student=student_query)
        
        submission = None
        if submission_query.exists():
            submission = submission_query.all()[0]
        else:
            submission = Submission.objects.create(question=question, taken_exam=taken_exam)
            submission.save()

        map(lambda choice: choice.delete(), submission.choices.all())
        for choice in submission_json['choices']:
            choice = Choice.objects.create(text = choice)
            choice.save()
            submission.choices.add(choice)
           
        submission.save()    
        return upsert_success_json_model(submission.id)
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
