"""only has 1 method, 
POST, you post token id and it grades the submissions related with the token"""

import api.helpers.endpoint_checks as endpoint_checks
from seat.models.token import Token
from seat.models.taken_exam import TakenExam, Submission
from seat.models.exam import Question
from django.http import HttpResponseServerError, JsonResponse, HttpResponseBadRequest
import logging

logger = logging.getLogger("api")

def grade_success_json(count):
    return JsonResponse({
        'success' : True,
        'error' : False,
        'count' : count
    })

def grade_failure_json(message):
    return JsonResponse({
        'success' : False,
        'error' : True,
        'message': message
    })

def choice_is_one_of(choice, answers):
    for answer in answers:
        if str(choice.text).strip().lower() == answer.text.strip().lower():
            return True
    logger.debug("wrong answer "+choice.text)
    return False

def grade_exam(taken_exam, question_map):
    
    submissions_for_exam = Submission.objects.filter(taken_exam=taken_exam).all()
    taken_exam.score = 0
    for submission in submissions_for_exam:
        answers = question_map[submission.question.id].answers.all()
        selections = submission.choices.all()
        # do not regrade questions
        # note that a resubmission should make the question no longer graded
        if submission.graded:
            if submission.correct:
                taken_exam.score += submission.question.points
            continue

        if answers.count() == 0:
            logger.debug("cannot grade this question, continuing")
        elif answers.count() == selections.count():
            # user choice count must be equal to number of answers
            counter = answers.count()
            for selection in selections:
                if choice_is_one_of(selection, answers):
                    counter -= 1
            submission.graded = True
            if counter == 0: # they got them all right
                submission.correct = True
        else:
            submission.graded = True
            submission.correct = False
            logger.debug("number of answers not equal to number of choices, auto fail")

        if submission.correct:
            taken_exam.score += submission.question.points
        submission.save()
    taken_exam.save()

def assign_to_own_id_in_map(question_map, question):
    question_map[question.id] = question

def grade_logic(teacher_query, request):
    try:
        token_id = token=request.POST.get('token_id')

        if not endpoint_checks.id_is_valid(token_id):
            return HttpResponseBadRequest("Invalid token_id")

        token_query = Token.objects.filter(exam__course__teacher=teacher_query, id=token_id)
        if not token_query.exists():
            return grade_failure_json("Token not found")
        
        closed_token_query = token_query.filter(open=False)

        if not closed_token_query.exists():
            return grade_failure_json("That token is still open! Please close the token to grade.")

        token = closed_token_query.all()[0]

        taken_exams_to_grade = TakenExam.objects.filter(exam__course__teacher=teacher_query, token=token)

        questions_for_exam = Question.objects.filter(exam=token.exam).all()

        question_map = {}

        map(lambda question: assign_to_own_id_in_map(question_map, question), questions_for_exam)

        map(lambda taken_exam: grade_exam(taken_exam, question_map), taken_exams_to_grade.all())

        return grade_success_json(taken_exams_to_grade.count())

    except Exception as error:
        logger.warn(str(error))
        return HttpResponseServerError("server error")

def grade(request):
    return endpoint_checks.standard_teacher_endpoint(
        "grade",
        ['token_id'],
        'POST',
        request,
        grade_logic)