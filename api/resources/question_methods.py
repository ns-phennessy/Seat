from seat.applications.seat_application import TeacherApplication, EditExamApplication
from django.http import JsonResponse
import json

editExamApplication = EditExamApplication()

def create_question_success_json_model(id):
    return JsonResponse({
        'success': True,
        'error': False,
        'id': str(id)
    })

# POST
def create_question(request):
    # TODO: tell Pat I need an exam ID (generated when page loaded)
    exam_data = json.loads(request.body)
    exam = editExamApplication.get_exam_by_id(exam_data['exam_id'])
    new_question = editExamApplication.create_question(exam_data['question'])
    new_question.save()
    exam.questions.add(new_question)
    return create_question_success_json_model(new_question.id)
