from django.shortcuts import render
import student.student_view_models as models
from seat.models.exam import Question
from seat.applications.RoutingApplication import RoutingApplication
from seat.applications.AuthenticationApplication import AuthenticationApplication
from seat.applications.StudentApplication import StudentApplication
from seat.applications.ExamApplication import ExamApplication
from seat.applications.TokenApplication import TokenApplication
from seat.models.student import Student

routingApplication = RoutingApplication()
authenticationApplication = AuthenticationApplication()
studentApplication = StudentApplication()
examApplication = ExamApplication()
tokenApplication = TokenApplication()

def index(request):
    if 'user_id' not in request.session:
        # user not allowed here, kick em out
        return routingApplication.logout(request)
    student_query = Student.objects.filter(id=request.session.get('user_id'))
    if not student_query.exists():
        # user is not allowed here, kick em out
        return routingApplication.logout(request)

    student = student_query.all()[0]

    released_taken_exams = studentApplication.get_released_past_exams(student)
    # to be sure the model can iterate over it
    # in case it isn't a list
    if not released_taken_exams:
        released_taken_exams = []

    # student dashboard
    return render(request, 'student/index.html', models.index_view_model(student, released_taken_exams))

def take_exam(request):
    if 'user_id' not in request.session: # set when logged in
        return routingApplication.logout(request)
    
    if 'token' not in request.session: # set when the token was validated
        return routingApplication.logout(request)
    
    student_query = Student.objects.filter(id=request.session.get('user_id'))
    if not student_query.exists():
        # user is not allowed here, kick em out
        return routingApplication.logout(request)
    
    token = tokenApplication.is_valid(request.session['token'])

    if not token:
        return routingApplication.invalid_permissions(request, "token not valid")

    exam = token.exam
    questions = Question.objects.filter(exam=exam)
    return render(request, 'student/exam.html', { 'student': student_query.all()[0], 'exam':exam, 'questions':questions, 'taking_exam':True})