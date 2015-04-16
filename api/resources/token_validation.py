"""only has 1 method, 
POST, you post tokens and it says yay or nay"""

import api.helpers.endpoint_checks as endpoint_checks
from seat.models.token import Token
from django.http import HttpResponseServerError, JsonResponse

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
        token_set = Token.objects.filter(token=request.POST['token']).all()
        if not token_set:
            return validate_token_failure_json_model("invalid token")
        token = token_set[0]
        if not token.open:
            return validate_token_failure_json_model("token not open anymore")
        else:
            request.session['token'] = request.POST['token']
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