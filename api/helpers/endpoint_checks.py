"""
If you are trying to understand how to use the API, this is the wrong file.
This file contains generic request validation which applies to broad categories
of requests, e.g. requests from teachers, or requests from students

This stuff exists just so we don't have to type it over and over
"""

from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError, HttpResponseNotAllowed
from seat.models.teacher import Teacher
from seat.models.student import Student
import logging

logger = logging.getLogger('api')

ID_MAX = 214748364

def get_dict_by_method(request, method):
    if method == "POST": return request.POST
    if method == "GET": return request.GET
    if method == "DELETE": return request.DELETE
    if method == "PUT": return request.PUT

def id_is_valid(id):
    return (id is not None and str(id).strip() != '' and int(id) < ID_MAX)

def key_is_substring_of_some_dict_key(key, dictionary):
    for dict_key in dictionary.keys():
        if dict_key.find(key) >= 0:
            return True
    return False

def all_required_values_present(values, request, method):
    dictionary = get_dict_by_method(request, method)
    for key in values:
        if not key_is_substring_of_some_dict_key(key, dictionary):
            return False
    return True

def standard_student_endpoint(
endpoint_name,
required_values,
method,
request,
functor):
    """
    # @required_values = array of necessary values for the endpoint to function
    # @method = POST, PUT, GET, DELETE
    # @request = request object from django
    #
    # @functor = function that actually does the 
    #            specific logic for this endpoint;
    #            takes (student_query, request) as params
    """        
    try:

        # verify method
        if request.method != method:
            logger.warn("non-"+method+" request landed in "+method+" logic at "+endpoint_name+" in the api")
            return HttpResponseBadRequest("bummer. your non-"+method+" request landed in the "+method+" logic.")
           
        # very if potentially authorized
        # user_id is only placed in the session by us
        # when the user logs into the application
        if 'user_id' not in request.session:
            logger.debug("unauthenticated request to "+endpoint_name)
            return HttpResponseForbidden('not authenticated')
                
        user_id = request.session.get('user_id')

        # verify the user id is regular
        if id_is_valid(user_id):
            logger.debug("invalid id in request to"+endpoint_name)
            return HttpResponseBadRequest("Invalid ID")
            
        # verify each of the desired parameters is present in the method body
        if not all_required_values_present(required_values, request, method):
            logger.info("bad request made to "+endpoint_name+", not enough params "+str(request))
            return HttpResponseBadRequest("expected more values, expected these:"+str(required_values))

        # get the query for the student
        student_query = Student.objects.filter(id=user_id)
                
        # verify that this requesting user actually exists
        if not student_query.exists():
            logger.info("user who was not a student made a request to "+endpoint_name+", id of user:"+str(request.session['user_id']))
            return HttpResponseNotAllowed('not authorized')
            
        # endpoint specific logic
        return functor(student_query, request)

    except Exception, error:
        logger.info("error in api endpoint "+endpoint_name+":"+str(error))
        return HttpResponseServerError("unhandled error")

def standard_teacher_endpoint(
endpoint_name,
required_values,
method,
request,
functor):
    """
    # @required_values = array of necessary values for the endpoint to function
    # @method = POST, PUT, GET, DELETE
    # @request = request object from django
    #
    # @functor = function that actually does the 
    #            specific logic for this endpoint;
    #            takes (teacher_query, request) as params
    """
    try:
        # validate we are receiving expected method
        if request.method != method:
            logger.warn("non-"+method+" request landed in "+method+" logic at "+endpoint_name+" in the api:"+str(request))
            return HttpResponseBadRequest("bummer. your non-"+method+" request landed in the "+method+" logic.")

        # validate that the user may be authorized to 
        # perform this action - we set the user_id in the
        # session at login
        if 'user_id' not in request.session:
            logger.debug("unauthenticated request to "+endpoint_name)
            return HttpResponseForbidden('not authenticated')

        teacher_id = request.session.get('user_id')

        # check that the id is valid for usage
        if not id_is_valid(teacher_id):
            return HttpResponseBadRequest("invalid id")

        # get the query for this teacher
        teacher_query = Teacher.objects.filter(id=teacher_id)

        # validate that there is some teacher with this id
        if not teacher_query.exists():
            logger.info("user who was not a teacher made a request to "+endpoint_name+", id of user:"+str(teacher_id))
            return HttpResponseForbidden('not a teacher!')

        # validate that all desired parameters are present in the request body
        if not all_required_values_present(required_values, request, method):
            logger.info("bad request made to "+endpoint_name+", not enough params ")
            return HttpResponseBadRequest("expected more values, expected these:"+str(required_values))
        
        # perform the endpoint specific logic
        return functor(teacher_query, request)
    except Exception, error:
        logger.info("error in api endpoint "+endpoint_name+":"+str(error))
        return HttpResponseServerError("unhandled error?!")