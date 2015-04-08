from seat.applications.seat_application import TeacherApplication, CourseApplication
from seat.models.teacher import Teacher
from seat.models.exam import Course
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

def create_exam_success_json_model(id):
    return JsonResponse({
        'success' : True,
        'error' : False,
        'id' : str(id)
    })
def create_exam_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

# POST
def create_exam(request):
    try:
        required_values = ['name', 'course_id']
        if request.method != 'POST':
            logger.warn("non-post request landed in post logic at create_exam in the api:"+str(request))
            return HttpResponseBadRequest("bummer. your non-post request landed in the post logic.")
        else:
            if 'user_id' not in request.session:
                logger.debug("unauthenticated request to create_exam:"+str(request))
                return HttpResponseForbidden('not authenticated')
            teacher = teacherApplication.get_teacher_by_id( request.session['user_id'] )

            if not teacher:
                logger.info("user who was not a teacher made a request to create_exam, id of user:"+str(request.session['user_id']))
                return HttpResponseForbidden('not a teacher!')

            if not all_required_values_present(required_values, request.POST):
                logger.info("bad request made to create_exam, not enough params "+str(request))
                return HttpResponseBadRequest("expected more values, expected these:"+str(required_values))
            else:
                try:
                    course_id = request.POST['course_id']
                    course = courseApplication.get_course_by_id(course_id)
                    new_exam = courseApplication.create_exam(course, request.POST['name'])
                    return create_exam_success_json_model(new_exam.id)
                except Exception, error:
                    logger.warn("problem creating exam! :"+str(error))
                    return create_exam_failure_json_model('failed to create the exam, sorry. This is probably a db error.')
    except Exception, error:
        logger.info("error in api endpoint create_exam:"+str(error))
        return HttpResponseServerError("unhandled error when creating the exam!")

def delete_exam_success_json_model():
    return JsonResponse({
        'success' : True,
        'error' : False,
    })
def delete_exam_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })
# DELETE
def delete_exam(request):
    try:
        required_values = ['exam_id']
        if request.method != 'POST':
            logger.warn("non-delete request landed in delete logic at delete_exam in the api:"+str(request))
            return HttpResponseBadRequest("bummer. your non-delete request landed in the delete logic.")
        else:
            if 'user_id' not in request.session:
                logger.debug("unauthenticated request to delete_exam:"+str(request))
                return HttpResponseForbidden('not authenticated')
            teacher = teacherApplication.get_teacher_by_id( request.session['user_id'] )

            if not teacher:
                logger.info("user who was not a teacher made a request to delete_exam, id of user:"+str(request.session['user_id']))
                return HttpResponseForbidden('not a teacher!')

            if not all_required_values_present(required_values, request.POST):
                logger.info("bad request made to delete_exam, not enough params "+str(request))
                return HttpResponseBadRequest("expected more values, expected these:"+str(required_values))
            else:
                try:
                    exam_id = request.POST['exam_id']
                    examApplication.delete_exam(exam_id)
                    return delete_exam_success_json_model()
                except Exception, error:
                    logger.warn("problem deleting exam! :"+str(error))
                    return delete_exam_failure_json_model('failed to delete the exam, sorry. This is probably a db error.')
    except Exception, error:
        logger.info("error in api endpoint delete_exam:"+str(error))
        return HttpResponseServerError("unhandled error when deleting the exam!")

def update_exam_success_json_model():
    return JsonResponse({
        'success' : True,
        'error' : False,
    })
def update_exam_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })
# PUT
def update_exam(request):
    try:
        required_values = ['exam_id', 'name']
        if request.method != 'PUT':
            logger.warn("non-put request landed in put logic at update_exam in the api:"+str(request))
            return HttpResponseBadRequest("bummer. your non-put request landed in the put logic.")
        else:
            if 'user_id' not in request.session:
                logger.debug("unauthenticated request to update_exam:"+str(request))
                return HttpResponseForbidden('not authenticated')
            teacher = teacherApplication.get_teacher_by_id( request.session['user_id'] )

            if not teacher:
                logger.info("user who was not a teacher made a request to update_exam, id of user:"+str(request.session['user_id']))
                return HttpResponseForbidden('not a teacher!')

            if not all_required_values_present(required_values, request.PUT):
                logger.info("bad request made to update_exam, not enough params "+str(request))
                return HttpResponseBadRequest("expected more values, expected these:"+str(required_values))
            else:
                try:
                    exam_id = request.PUT['exam_id']
                    exam = examApplication.get_exam_by_id(exam_id)
                    exam.name = request.PUT['name']
                    exam.save()
                    return update_exam_success_json_model()
                except Exception, error:
                    logger.warn("problem updating exam! :"+str(error))
                    return update_exam_failure_json_model('failed to update the exam, sorry. This is probably a db error.')
    except Exception, error:
        logger.info("error in api endpoint update_exam:"+str(error))
        return HttpResponseServerError("unhandled error when updating the exam!")


def get_exam_success_json_model(exam):
    return JsonResponse({
        'success' : True,
        'error' : False,
        'exam' : {
            'name' : exam.name,
            'id'   : exam.id
        }
    })
def get_exam_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

# GET
def get_exam(request):
    try:
        required_values = ['exam_id']
        if request.method != 'GET':
            logger.warn("non-post request landed in post logic at get_exam in the api:"+str(request))
            return HttpResponseBadRequest("bummer. your non-post request landed in the post logic.")
        else:
            if 'user_id' not in request.session:
                logger.debug("unauthenticated request to get_exam:"+str(request))
                return HttpResponseForbidden('not authenticated')
            teacher = teacherApplication.get_teacher_by_id( request.session['user_id'] )

            if not teacher:
                logger.info("user who was not a teacher made a request to get_exam, id of user:"+str(request.session['user_id']))
                return HttpResponseForbidden('not a teacher!')

            if not all_required_values_present(required_values, request.GET):
                logger.info("bad request made to get_exam, not enough params "+str(request))
                return HttpResponseBadRequest("expected more values, expected these:"+str(required_values))
            else:
                try:
                    exam_id = request.GET['exam_id']
                    exam = examApplication.get_exam_by_id(exam_id)
                    return get_exam_success_json_model(exam)
                except Exception, error:
                    logger.warn("problem getting exam! :"+str(error))
                    return get_exam_failure_json_model('failed to get the exam, sorry. This is probably a db error.')
    except Exception, error:
        logger.info("error in api endpoint get_exam:"+str(error))
        return HttpResponseServerError("unhandled error when getting the exam!")

