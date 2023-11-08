from django.core.exceptions import PermissionDenied

def user_is_lessor(function):

    def wrap(request, *args, **kwargs):   

        if request.user.role == 'lessor':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap



def user_is_customer(function):

    def wrap(request, *args, **kwargs):    

        if request.user.role == 'customer':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap