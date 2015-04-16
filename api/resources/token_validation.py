"""only has 1 method, 
POST, you post tokens and it says yay or nay"""

import api.helpers.endpoint_checks as endpoint_checks
from seat.models.token import Token
from django.http import HttpResponseServerError

def validate_token_success_json_model(exam_id):
    return JsonResponse({
        'success' : True,
        'error' : False,
        'exam_id': exam_id
    })

def validate_token_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def validate_token_logic(student, request):
    try:
        token = Token.objects.get(token=request['token'])
        if not token:
            return validate_token_failure_json_model("invalid token")
        elif not token.open:
            return validate_token_failure_json_model("token not open anymore")
        else:
            request.session['token'] = request['token']
            return validate_token_success_json_model(token.exam.id)
    except Exception as error:
        return HttpResponseServerError("server error")
def validate_token(request):
    return endpoint_checks.standard_student_endpoint(
        "validate_token",
        ['token'],
        'POST',
        request,
        validate_token_logic)