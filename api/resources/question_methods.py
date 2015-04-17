from seat.applications.TeacherApplication import TeacherApplication
from seat.applications.QuestionApplication import QuestionApplication
from django.http import JsonResponse
from api.helpers import endpoint_checks
import json
import logging

logger = logging.getLogger(__name__)

questionApplication = QuestionApplication()

# POST
def create_question_success_json_model(question_id):
    return JsonResponse({
        'success': True,
        'error': False,
        'id': str(question_id)
    })

def create_question_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def create_question_logic(teacher, request):
    try:
        #TODO test that teacher owns logic
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

# PUT
def update_question_success_json_model():
    return JsonResponse({
        'success': True,
        'error': False
    })

def update_question_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def update_question_logic(teacher, request):
    try:
        #TODO: test that teacher owns resource
        raise Exception("UNSUPPORTED")
    except Exception, error:
        logger.warn("problem updating question! :"+str(error))
        return update_question_failure_json_model('failed to update the question, sorry. This is probably a db error.')

def update_question(request):
    return endpoint_checks.standard_teacher_endpoint(
        "update_question",
        ['exam_id', 'question'],
        'POST',
        request,
        update_question_logic
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
