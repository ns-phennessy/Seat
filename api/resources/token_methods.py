from seat.applications.TeacherApplication import TeacherApplication
from seat.applications.QuestionApplication import QuestionApplication
from django.http import JsonResponse
from api.helpers import endpoint_checks
import json
import logging

logger = logging.getLogger('api')

tokenApplication = QuestionApplication()

# POST
def create_token_success_json_model(token_id):
    return JsonResponse({
        'success': True,
        'error': False,
        'id': str(token_id)#TODO: serialized token
    })

def create_token_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def create_token_logic(teacher, request):
    try:
        #TODO test that teacher owns logic
        raise Exception("UNSUPPORTED!!")
    except Exception, error:
        logger.warn("problem creating token! :"+str(error))
        return create_token_failure_json_model('failed to create the token, sorry. This is probably a db error.')

def create_token(request):
    return endpoint_checks.standard_teacher_endpoint(
        "create_token",
        ['exam_id'],
        'POST',
        request,
        create_token_logic
        )

# PUT
def update_token_success_json_model():
    return JsonResponse({
        'success': True,
        'error': False
    })

def update_token_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def update_token_logic(teacher, request):
    try:
        #TODO: test that teacher owns resource
        raise Exception("UNSUPPORTED")
    except Exception, error:
        logger.warn("problem updating token! :"+str(error))
        return update_token_failure_json_model('failed to update the token, sorry. This is probably a db error.')

def update_token(request):
    return endpoint_checks.standard_teacher_endpoint(
        "update_token",
        ['token_id'],
        'POST',
        request,
        update_token_logic
        )

# DELETE
def delete_token_success_json_model():
    return JsonResponse({
        'success': True,
        'error': False
    })

def delete_token_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def delete_token_logic(teacher, request):
    try:
        #TODO: test that teacher owns resource
        raise Exception("UNSUPPORTED")
    except Exception, error:
        logger.warn("problem deleting token! :"+str(error))
        return delete_token_failure_json_model('failed to delete the token, sorry. This is probably a db error.')

def delete_token(request):
    return endpoint_checks.standard_teacher_endpoint(
        "delete_token",
        ['token_id'],
        'POST',
        request,
        delete_token_logic
        )

# GET
def get_token_success_json_model():
    return JsonResponse({
        'success': True,
        'error': False
        #TODO: serialized token
    })

def get_token_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def get_token_logic(teacher, request):
    try:
        #TODO: test that teacher owns resource
        raise Exception("UNSUPPORTED")
    except Exception, error:
        logger.warn("problem getting token! :"+str(error))
        return get_token_failure_json_model('failed to get the token, sorry. This is probably a db error.')

def get_token(request):
    return endpoint_checks.standard_teacher_endpoint(
        "get_token",
        ['token_id'],
        'POST',
        request,
        get_token_logic
        )


