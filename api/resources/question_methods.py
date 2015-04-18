from seat.applications.TeacherApplication import TeacherApplication
from seat.applications.QuestionApplication import QuestionApplication
from django.http import JsonResponse
from api.helpers import endpoint_checks
import json
import logging

logger = logging.getLogger(__name__)

questionApplication = QuestionApplication()

# POST -- NOW UPSERT
def upsert_question_success_json_model(question_id):
    return JsonResponse({
        'success': True,
        'error': False,
        'id': str(question_id)
    })

def upsert_question_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def upsert_question_logic(teacher, request):
    try:
        #TODO test that teacher owns logic
        question = json.loads(request.POST.get('question'))
        exam_id = request.POST['exam_id']
        modified_question = questionApplication.upsert_question(exam_id, question)
        return upsert_question_success_json_model(modified_question.id)
    except Exception, error:
        logger.warn("problem upserting question! :"+str(error))
        return upsert_question_failure_json_model('failed to upsert the question, sorry. This is probably a db error.')

def upsert_question(request):
    return endpoint_checks.standard_teacher_endpoint(
        "upsert_question",
        ['exam_id', 'question'],
        'POST',
        request,
        upsert_question_logic
        )

# DELETE
def delete_question_success_json_model():
    return JsonResponse({
        'success': True,
        'error': False
    })

def delete_question_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def delete_question_logic(teacher, request):
    try:
        #TODO: test that teacher owns resource
        question_id = request.DELETE['question_id']
        questionApplication.delete_question(question_id)
        return delete_question_success_json_model()
    except Exception, error:
        logger.warn("problem deleting question! :"+str(error))
        return delete_question_failure_json_model('failed to delete the question, sorry. This is probably a db error.')

def delete_question(request):
    return endpoint_checks.standard_teacher_endpoint(
        "delete_question",
        ['question_id'],
        'DELETE',
        request,
        delete_question_logic
        )

# GET
def get_question_success_json_model():
    return JsonResponse({
        'success': True,
        'error': False
    })

def get_question_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def get_question_logic(teacher, request):
    try:
        #TODO: test that teacher owns resource
        raise Exception("UNSUPPORTED")
    except Exception, error:
        logger.warn("problem getting question! :"+str(error))
        return get_question_failure_json_model('failed to get the question, sorry. This is probably a db error.')

def get_question(request):
    return endpoint_checks.standard_teacher_endpoint(
        "get_question",
        ['exam_id', 'question'],
        'POST',
        request,
        get_question_logic
        )
