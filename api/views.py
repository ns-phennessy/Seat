from api.resources import course_methods

def course(request, course_id = None):
    if request.method == 'POST':
        return course_methods.create_course(request)
    elif request.method == 'PUT':
        return course_methods.update_course(request, course_id)
    elif request.method == 'DELETE':
        return course_methods.delete_course(request, course_id)
    elif request.method == 'GET':
        return course_methods.get_course(request, course_id)
    else:
        return HttpResponseBadRequest("unsupported method")