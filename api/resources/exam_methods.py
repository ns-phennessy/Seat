from seat.applications.TeacherApplication import TeacherApplication
from seat.applications.CourseApplication import CourseApplication
from seat.applications.ExamApplication import ExamApplication
from seat.models.course import Course
from django.http import JsonResponse
from api.helpers import endpoint_checks
from django.core.urlresolvers import reverse
import logging

logger = logging.getLogger('api')

teacherApplication = TeacherApplication()
courseApplication = CourseApplication()
examApplication = ExamApplication()

# POST
def create_exam_success_json_model(exam_id):
    return JsonResponse({
        'success' : True,
        'error' : False,
        'id' : str(exam_id),
        'edit_url': reverse('dashboard.views.exam_edit', args=[exam_id])
    })

def create_exam_failure_json_model(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message' : str(message)
    })

def create_exam_logic(teacher, request):
    try:
        course_id = request.POST['course_id']
        course = courseApplication.get_course_by_id(course_id)
        new_exam = courseApplication.create_exam(course, request.POST['name'])
        return create_exam_success_json_model(new_exam.id)
    except Exception, error:
        logger.warn("problem creating exam! :"+str(error))
        return create_exam_failure_json_model('failed to create the exam, sorry. This is probably a db error.') 

def create_exam(request):
    return endpoint_checks.standard_teacher_endpoint(
        "create_exam",
        ['name', 'course_id'],
        'POST',
        request,
        create_exam_logic
        )

# DELETE
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

def delete_exam_logic(teacher, request):
    try:
        exam_id = request.DELETE['exam_id']
        examApplication.delete_exam(exam_id)
        return delete_exam_success_json_model()
    except Exception, error:
        logger.warn("problem deleting exam! :"+str(error))
        return delete_exam_failure_json_model('failed to delete the exam, sorry. This is probably a db error.')  

def delete_exam(request):
    return endpoint_checks.standard_teacher_endpoint(
        "delete_exam",
        ['exam_id'],
        'DELETE',
        request,
        delete_exam_logic
        )

# PUT
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

def update_exam_logic(teacher, request):
    try:
        exam_id = request.PUT['exam_id']
        exam = examApplication.get_exam_by_id(exam_id)
        exam.name = request.PUT['name']
        exam.save()
        return update_exam_success_json_model()
    except Exception, error:
        logger.warn("problem updating exam! :"+str(error))
        return update_exam_failure_json_model('failed to update the exam, sorry. This is probably a db error.')

def update_exam(request):
    return endpoint_checks.standard_teacher_endpoint(
        "update_exam",
        ['exam_id', 'name'],
        'PUT',
        request,
        update_exam_logic
        )
# GET
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

def get_exam_logic(teacher, request):
    try:
        exam_id = request.GET['exam_id']
        exam = examApplication.get_exam_by_id(exam_id)
        return get_exam_success_json_model(exam)
    except Exception, error:
        logger.warn("problem getting exam! :"+str(error))
        return get_exam_failure_json_model('failed to get the exam, sorry. This is probably a db error.')

def get_exam(request):
    return endpoint_checks.standard_teacher_endpoint(
        "get_exam",
        ['exam_id'],
        'GET',
        request,
        get_exam_logic
        )
