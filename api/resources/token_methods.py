from seat.applications.QuestionApplication import QuestionApplication
from seat.applications.TeacherApplication import TeacherApplication
from django.http import JsonResponse
from seat.models.token import Token
from seat.models.exam import Exam
from api.helpers import endpoint_checks
import logging

logger = logging.getLogger('api')

tokenApplication = QuestionApplication()

# POST
def create_token_success_json_model(token):
    return JsonResponse({
        'success': True,
        'error': False,
        'id': str(token.id),
        'token' : token.token
    })

def create_token_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def create_token_logic(teacher_query, request):
    try:
        # check that teacher has rights to this exam
        if not endpoint_checks.id_is_valid(request.POST.get('exam_id')):
            return create_token_failure_json_model("invalid id")

        exam_query = Exam.objects.filter(course__teacher=teacher_query, id=request.POST.get('exam_id'))
        
        # create token
        if exam_query.exists():
            token = Token.objects.create(exam=exam_query.all()[0])
            return create_token_success_json_model(token)
        
        # or fail
        return create_token_failure_json_model("exam does not exist")
    except Exception, error:
        logger.warn("problem creating token! :"+str(error))
        return create_token_failure_json_model('failed to create the token')

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

def update_token_logic(teacher_query, request):
    try:
        # validate the actual request
        token_json = json.dumps(request.get('token'))

        if 'open' not in token_json:
            return update_token_failure_json_model('need an open status')

        if 'released' not in token_json:
            return update_token_failure_json_model('need a released status')

        token_is_open = token_json.get('open')
        token_is_released = token_json.get('released')
        token_id = token_json.get('token_id')

        if not endpoint_checks.id_is_valid(token_id):
            return update_token_failure_json_model('token is not valid')

        if token_is_open is not True or False:
            return update_token_failure_json_model('open status must be true or false')

        if token_is_released is not True or False:
            return update_token_failure_json_model('released status must be true or false')



        # is the teacher authorized? get the token if so
        token_query = Token.objects.filter(exam__course__teacher=teacher_query, id=request.session.get('token_id'))
        
        # has it been found?
        if not token_query.exists():
            return update_token_failure_json_model('token not found')

        token = token_query.all()[0]

        token.open = token_is_open
        token.released = token_is_released

        token.save()
        return update_token_success_json_model()
            
    except Exception, error:
        logger.warn("problem updating token! :"+str(error))
        return update_token_failure_json_model('failed to update the token')

def update_token(request):
    return endpoint_checks.standard_teacher_endpoint(
        "update_token",
        ['token'],
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

def delete_token_logic(teacher_query, request):
    try:
        token_id = request.session('token_id')
        if endpoint_checks.id_is_valid(token_id):
            return delete_token_failure_json_model('invalid id')

        token_query = Token.objects.filter(exam__course__teacher=teacher_query, id=token_id)
        
        if not token_query.exists():
            return delete_token_failure_json_model('token does not exist')

        token_query.update(deleted=True)
    
        return delete_token_success_json_model()

    except Exception as error:
        logger.warn("problem deleting token! :"+str(error))
        return delete_token_failure_json_model('failed to delete the token')

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
        return get_token_failure_json_model('failed to get the token')

def get_token(request):
    return endpoint_checks.standard_teacher_endpoint(
        "get_token",
        ['token_id'],
        'POST',
        request,
        get_token_logic
        )


