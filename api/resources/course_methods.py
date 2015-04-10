from seat.applications.seat_application import TeacherApplication, CourseApplication
from seat.models.teacher import Teacher
from seat.models.course import Course
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError, JsonResponse
from api.helpers import endpoint_checks
import logging

logger = logging.getLogger('api')

teacherApplication = TeacherApplication()
courseApplication = CourseApplication()

def all_required_values_present(values, dict):
    for key in values:
        if key not in dict:
            return False
    return True

# POST 
def create_course_success_json_model(id):
    return JsonResponse({
        'success' : True,
        'error' : False,
        'id' : str(id)
    })
def create_course_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def create_course_logic(teacher, request):
    try:
        new_course = teacherApplication.create_course(teacher, request.POST['name'])
        return create_course_success_json_model(new_course.id)
    except Exception, error:
        logger.warn("problem creating course! :"+str(error))
        return create_course_failure_json_model('failed to create the course, sorry. This is probably a db error.')

def create_course(request):
    return endpoint_checks.standard_teacher_endpoint(
        "create_course",
        ['name'],
        'POST',
        request,
        create_course_logic
        )

# DELETE
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
def delete_course_logic(teacher, request):
    try:
        teacherApplication.delete_course(teacher, request.DELETE['course_id'])
        return delete_course_success_json_model()
    except Exception, error:
        logger.warn("problem deleting course! :"+str(error))
        return delete_course_failure_json_model('failed to delete the course, sorry. This is probably a db error.')

def delete_course(request):
    return endpoint_checks.standard_teacher_endpoint(
        "delete_course",
        ['course_id'],
        'DELETE',
        request,
        delete_course_logic
        )

# PUT
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

def update_course_logic(teacher, request):
    try:
        # presently only the name can be updated
        new_course = teacherApplication.update_course(teacher, request.PUT['course_id'], request.PUT['name'])
        return update_course_success_json_model()
    except Exception, error:
        logger.warn("problem updating course! :"+str(error))
        return update_course_failure_json_model('failed to update the course, sorry. This is probably a db error.')

def update_course(request):
    return endpoint_checks.standard_teacher_endpoint(
        "update_course",
        ['course_id','name'],
        'PUT',
        request,
        update_course_logic
        )

# GET
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

def get_course_logic(teacher, request):
    try:
        course = courseApplication.get_course_by_id(course_id)
        return get_course_success_json_model(course)
    except Exception, error:
        logger.warn("problem getting course! :"+str(error))
        return get_course_failure_json_model('failed to get the course, sorry. This is probably a db error.') 

def get_course(request):
    return endpoint_checks.standard_teacher_endpoint(
        "get_course",
        ['course_id'],
        'GET',
        request,
        update_course_logic
        )  

