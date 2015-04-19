from seat.applications.AuthenticationApplication import AuthenticationApplication
from seat.applications.TeacherApplication import TeacherApplication
from seat.models.course import Course
from django.http import JsonResponse
from api.helpers import endpoint_checks
import logging

logger = logging.getLogger('api')

teacherApplication = TeacherApplication()
authenticationApplication = AuthenticationApplication()

def all_required_values_present(values, dictionary):
    for key in values:
        if key not in dictionary:
            return False
    return True

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

def create_course_logic(teacher, request):
    try:
        new_course, msg = teacherApplication.create_course(teacher, request.POST['name'])
        if not new_course:
            return create_course_failure_json_model(msg)
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
        success, msg = teacherApplication.delete_course(teacher, request.DELETE['course_id'])
        if not success:
            return delete_course_failure_json_model(msg)
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
        success, msg = teacherApplication.update_course(teacher, request.PUT['course_id'], request.PUT['name'])
        if not success:
            return update_course_failure_json_model(msg)
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
        course = Course.objects.filter(course=request.GET.get('course_id'), teacher=teacher)
        if not course.exists():
            return get_course_failure_model("course did not exist")
        return get_course_success_json_model(course.all()[0])
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

