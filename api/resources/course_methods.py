from seat.applications.seat_application import TeacherApplication, CourseApplication
from seat.models.teacher import Teacher
from seat.models.course import Course
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError, JsonResponse
import logging

logger = logging.getLogger('api')

teacherApplication = TeacherApplication()
courseApplication = CourseApplication()

def all_required_values_present(values, dict):
    for key in values:
        if key not in dict:
            return False
    return True

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

# POST
def create_course(request):
    try:
        required_values = ['name']
        if request.method != 'POST':
            logger.warn("non-post request landed in post logic at create_course in the api:"+str(request))
            return HttpResponseBadRequest("bummer. your non-post request landed in the post logic.")
        else:
            if 'user_id' not in request.session:
                logger.debug("unauthenticated request to create_course:"+str(request))
                return HttpResponseForbidden('not authenticated')
            teacher = teacherApplication.get_teacher_by_id( request.session['user_id'] )

            if not teacher:
                logger.info("user who was not a teacher made a request to create_course, id of user:"+str(request.session['user_id']))
                return HttpResponseForbidden('not a teacher!')

            if not all_required_values_present(required_values, request.POST):
                logger.info("bad request made to create_course, not enough params "+str(request))
                return HttpResponseBadRequest("expected more values, expected these:"+str(required_values))
            else:
                try:
                    new_course = teacherApplication.create_course(teacher, request.POST['name'])
                    return create_course_success_json_model(new_course.id)
                except Exception, error:
                    logger.warn("problem creating course! :"+str(error))
                    return create_course_failure_json_model('failed to create the course, sorry. This is probably a db error.')
    except Exception, error:
        logger.info("error in api endpoint create_course:"+str(error))
        return HttpResponseServerError("unhandled error when creating the course!")


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
# DELETE
def delete_course(request, course_id):
    try:
        required_values = []
        if request.method != 'DELETE':
            logger.warn("non-delete request landed in delete logic at delete_course in the api:"+str(request))
            return HttpResponseBadRequest("bummer. your non-delete request landed in the delete logic.")
        else:
            if 'user_id' not in request.session:
                logger.debug("unauthenticated request to delete_course:"+str(request))
                return HttpResponseForbidden('not authenticated')
            teacher = teacherApplication.get_teacher_by_id( request.session['user_id'] )

            if not teacher:
                logger.info("user who was not a teacher made a request to delete_course, id of user:"+str(request.session['user_id']))
                return HttpResponseForbidden('not a teacher!')

            if not all_required_values_present(required_values, request.DELETE):
                logger.info("bad request made to delete_course, not enough params "+str(request))
                return HttpResponseBadRequest("expected more values, expected these:"+str(required_values))
            else:
                try:
                    new_course = teacherApplication.delete_course(teacher, course_id)
                    return delete_course_success_json_model()
                except Exception, error:
                    logger.warn("problem deleting course! :"+str(error))
                    return delete_course_failure_json_model('failed to delete the course, sorry. This is probably a db error.')
    except Exception, error:
        logger.info("error in api endpoint delete_course:"+str(error))
        return HttpResponseServerError("unhandled error when deleting the course!")

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
# PUT
def update_course(request, course_id):
    try:
        required_values = ['name']
        if request.method != 'PUT':
            logger.warn("non-put request landed in logic at update_course in the api:"+str(request))
            return HttpResponseBadRequest("bummer. your non-update request landed in the update logic.")
        else:
            if 'user_id' not in request.session:
                logger.debug("unauthenticated request to update_course:"+str(request))
                return HttpResponseForbidden('not authenticated')
            teacher = teacherApplication.get_teacher_by_id( request.session['user_id'] )

            if not teacher:
                logger.info("user who was not a teacher made a request to update_course, id of user:"+str(request.session['user_id']))
                return HttpResponseForbidden('not a teacher!')

            if not all_required_values_present(required_values, request.PUT):
                logger.info("bad request made to update_course, not enough params "+str(request))
                return HttpResponseBadRequest("expected more values, expected these:"+str(required_values))
            else:
                try:
                    # presently only the name can be updated
                    new_course = teacherApplication.update_course(teacher, course_id, name)
                    return update_course_success_json_model()
                except Exception, error:
                    logger.warn("problem updating course! :"+str(error))
                    return update_course_failure_json_model('failed to update the course, sorry. This is probably a db error.')
    except Exception, error:
        logger.info("error in api endpoint update_course:"+str(error))
        return HttpResponseServerError("unhandled error when updating the course!")  


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

# GET
def get_course(request, course_id):
    try:
        required_values = []
        if request.method != 'GET':
            logger.warn("non-get request landed in logic at get_course in the api:"+str(request))
            return HttpResponseBadRequest("bummer. your non-get request landed in the get logic.")
        else:
            if 'user_id' not in request.session:
                logger.debug("unauthenticated request to get_course:"+str(request))
                return HttpResponseForbidden('not authenticated')
            teacher = teacherApplication.get_teacher_by_id(request.session['user_id'] )

            if not teacher:
                logger.info("user who was not a teacher made a request to get_course, id of user:"+str(request.session['user_id']))
                return HttpResponseForbidden('not a teacher!')

            if not all_required_values_present(required_values, request.GET):
                logger.info("bad request made to get_course, not enough params "+str(request))
                return HttpResponseBadRequest("expected more values, expected these:"+str(required_values))
            else:
                try:
                    course = courseApplication.get_course_by_id(course_id)
                    return get_course_success_json_model(course)
                except Exception, error:
                    logger.warn("problem getting course! :"+str(error))
                    return get_course_failure_json_model('failed to get the course, sorry. This is probably a db error.')
    except Exception, error:
        logger.info("error in api endpoint get_course:"+str(error))
        return HttpResponseServerError("unhandled error when getting the course!")  

