from seat.applications.seat_application import TeacherApplication, QuestionApplication
from django.http import JsonResponse
from api.helpers import endpoint_checks
import json
import logging

logger = logging.getLogger('api')

questionApplication = QuestionApplication()

# POST
def create_question_success_json_model(id):
    return JsonResponse({
        'success': True,
        'error': False,
        'id': str(id)
    })

def create_question_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def create_question_logic(teacher, request):
    try:
        question = json.loads(request.POST.get('question'))
        exam_id = request.POST['exam_id']
        new_question = questionApplication.create_question(exam_id, question)
        return create_question_success_json_model(new_question.id)
    except Exception, error:
        logger.warn("problem creating question! :"+str(error))
        return create_question_failure_json_model('failed to create the question, sorry. This is probably a db error.')

def create_question(request):
    return endpoint_checks.standard_teacher_endpoint(
        "create_question",
        ['exam_id', 'question'],
        'POST',
        request,
        create_question_logic
        )
