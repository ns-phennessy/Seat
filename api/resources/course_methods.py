from seat.applications.AuthenticationApplication import AuthenticationApplication
from seat.applications.TeacherApplication import TeacherApplication
from seat.models.course import Course
from django.http import JsonResponse
from api.helpers import endpoint_checks
import logging

logger = logging.getLogger('api')

teacherApplication = TeacherApplication()
authenticationApplication = AuthenticationApplication()

# POST 
def create_course_success_json_model(course_id):
    return JsonResponse({
        'success' : True,
        'error' : False,
        'id' : str(course_id)
    })

def create_course_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })


def create_course_logic(teacher_query, request):
    """
    this is the endpoint specific logic
    for a POST to /api/course
    """
    try:

        # create course for this teacher
        # type: [ Course, str ]
        new_course, msg = teacherApplication.create_course(teacher_query.all()[0], request.POST['name'])

        # check that the course was created
        if new_course is None:
            return create_course_failure_json_model(msg)

        # return the new course id
        return create_course_success_json_model(new_course.id)

    except Exception, error:

        logger.warn("problem creating course! :"+str(error))
        return create_course_failure_json_model('system failed to create the course.')

def create_course(request):
    """
    this is the initial method called when
    a post request hits the server
   
    the second argument is the list of top level required
    arguments in the request body parameters
    for example, here ['name'] is given, and it
    is expected to be a POST request (3rd arg), so

    the endpoint check will check that request.POST['name'] exists.

    finally, if the endpoint check is satisfied, it will execute
    the create course logic above
    """
    return endpoint_checks.standard_teacher_endpoint(
        "create_course",
        ['name'],
        'POST',
        request,
        create_course_logic
        )

def delete_course_success_json_model():
    return JsonResponse({
        'success' : True,
        'error' : False,
    })
def delete_course_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def delete_course_logic(teacher_query, request):
    """
    POST to /api/course with 
    X-METHODOVERRIDE="DELETE" header
    """
    try:

        # types: [ bool, str ]
        success, msg = teacherApplication.delete_course(teacher_query, request.DELETE['course_id'])

        # failure json if we failed
        if not success:
            return delete_course_failure_json_model(msg)

        # return success json
        return delete_course_success_json_model()

    except Exception, error:

        logger.warn("problem deleting course! :"+str(error))
        return delete_course_failure_json_model('failed to delete the course, sorry. This is probably a db error.')


def delete_course(request):
    """
    this is the initial method called when
    a post request hits the server with
    a header X-METHODOVERRIDE="DELETE".

    the second argument is the list of top level required
    arguments in the request body parameters
    for example, here ['course_id'] is given, and it
    is expected to be a DELETE request (3rd arg), so

    the endpoint check will check that request.DELETE['course_id'] exists.

    finally, if the endpoint check is satisfied, it will execute
    the create course logic above
    """
    return endpoint_checks.standard_teacher_endpoint(
        "delete_course",
        ['course_id'],
        'DELETE',
        request,
        delete_course_logic
        )

def update_course_success_json_model():
    return JsonResponse({
        'success' : True,
        'error' : False,
    })
def update_course_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })


def update_course_logic(teacher_query, request):
    """
    PUT /api/course 
    header: X-METHODOVERRIDE = "PUT"
    """
    try:
        
        # try to update the course
        # [ bool, str ]
        success, msg = teacherApplication.update_course(teacher_query, request.PUT['course_id'], request.PUT['name'])
        
        # sadpath
        if not success:
            return update_course_failure_json_model(msg)
        
        # return success json
        return update_course_success_json_model()
    
    except Exception, error:
        logger.warn("problem updating course! :"+str(error))
        return update_course_failure_json_model('failed to update the course, sorry. This is probably a db error.')


def update_course(request):
    """
    this is the initial method called when
    a post request hits the server with
    a header X-METHODOVERRIDE="PUT".

    the second argument is the list of top level required
    arguments in the request body parameters:
    for example, here ['course_id', 'name'] is given, and it
    is expected to be a PUT request (3rd arg), so

    the endpoint check will check that request.PUT['course_id'] exists,
    and that request.PUT['name'] exists

    finally, if the endpoint check is satisfied, it will execute
    the create course logic above
    """
    return endpoint_checks.standard_teacher_endpoint(
        "update_course",
        ['course_id','name'],
        'PUT',
        request,
        update_course_logic
        )

def get_course_success_json_model(course):
    return JsonResponse({
        'success' : True,
        'error' : False,
        'course' : {
            'name' : course.name,
            'id'   : course.id
        }
    })

def get_course_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def get_course_logic(teacher_query, request):
    """
    GET /api/course
    """
    try:
        # query for the course
        course = Course.objects.filter(course=request.GET.get('course_id'), teacher=teacher_query)

        # nope, not found
        if not course.exists():
            return get_course_failure_json_model("course did not exist")

        # send it on back
        return get_course_success_json_model(course.all()[0])

    except Exception, error:
        logger.warn("problem getting course! :"+str(error))
        return get_course_failure_json_model('failed to get the course, sorry. This is probably a db error.') 

def get_course(request):
    """
    this is the initial method called when
    a post request hits the server

    the second argument is the list of top level required
    arguments in the request body parameters:
    for example, here ['course_id'] is given, and it
    is expected to be a GET request (3rd arg), so

    the endpoint check will check that request.GET['course_id'] exists,
    and that request.GET['name'] exists

    finally, if the endpoint check is satisfied, it will execute
    the get course logic above
    """
    return endpoint_checks.standard_teacher_endpoint(
        "get_course",
        ['course_id'],
        'GET',
        request,
        update_course_logic
        )  

