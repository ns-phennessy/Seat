

class RoutingApplication(object):
    """object for abstracting out all those hardcoded urls"""

    def error_url(self, request):
        return '/500.html' #TODO: delete this when sure this route exists

    def invalid_permissions_url(self, request):
        return '/invalidpermissions/' #TODO

    def invalid_request_url(self, request):
        return '/invalidrequest/' #TODO:
    
    def teacher_index(self, request=None):
        """ indicates the default landing page for a teacher upon login """
        return '/dashboard/courses/'

    def student_index(self, request=None):
        """ indicates the default landing page for a student upon login """
        return '/student/'




