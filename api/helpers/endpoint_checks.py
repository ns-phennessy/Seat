from seat.applications.seat_application import TeacherApplication, CourseApplication
from seat.models.teacher import Teacher
from seat.models.course import Course
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError, JsonResponse
import logging

logger = logging.getLogger('api')

teacherApplication = TeacherApplication()
courseApplication = CourseApplication()

def get_dict_by_method(request, method):
    if method == "POST": return request.POST
    if method == "GET": return request.GET
    if method == "DELETE": return request.DELETE
    if method == "PUT": return request.PUT

def all_required_values_present(values, request, method):
    dict = get_dict_by_method(request, method)
    for key in values:
        if not key in dict:
            return False
    return True

# @required_values = array of necessary values for the endpoint to function
# @method = POST, PUT, GET, DELETE
# @request = request object from django
# @functor = function that actually does the functionality the request is intended for, takes teacher,request as param
def standard_teacher_endpoint(
    endpoint_name,
    required_values,
    method,
    request,
    functor):
        try:
            if request.method != method:
                logger.warn("non-"+method+" request landed in "+method+" logic at "+endpoint_name+" in the api:"+str(request))
                return HttpResponseBadRequest("bummer. your non-"+method+" request landed in the "+method+" logic.")
            else:
                if 'user_id' not in request.session:
                    logger.debug("unauthenticated request to "+endpoint_name+":"+str(request))
                    return HttpResponseForbidden('not authenticated')

                teacher = teacherApplication.get_teacher_by_id( request.session['user_id'] )

                if not teacher:
                    logger.info("user who was not a teacher made a request to "+endpoint_name+", id of user:"+str(request.session['user_id']))
                    return HttpResponseForbidden('not a teacher!')

                if not all_required_values_present(required_values, request, method):
                    logger.info("bad request made to "+endpoint_name+", not enough params "+str(request))
                    return HttpResponseBadRequest("expected more values, expected these:"+str(required_values))
                else:
                    return functor(teacher, request)
        except Exception, error:
            logger.info("error in api endpoint "+endpoint_name+":"+str(error))
            return HttpResponseServerError("unhandled error!")