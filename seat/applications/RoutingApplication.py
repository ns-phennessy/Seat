

class RoutingApplication:

    """object for abstracting out all those hardcoded urls"""

    def error_url(self, request):
        return '/500.html' #TODO: delete this when sure this route exists

    def invalid_permissions_url(self, request):
        return '/invalidpermissions/' #TODO

    def invalid_request_url(self, request):
        return '/invalidrequest/' #TODO(object):
    pass




