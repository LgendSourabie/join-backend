from rest_framework import permissions

class IsAuthenticatedOrNot(permissions.BasePermission):
    """
    Permission for enabling users to DELETE and/or UPDATE Data only 
    if they are owner of those data. 

    The admin user can GET all the data but cannot modified data of users.

    Every user has the right to POST data unless he/ she is authenticated.
    
    """

    def has_object_permission(self, request, view, obj):

        if request.method == "GET":
            return bool(request.user and  request.user == obj.author or request.user.is_superuser)
        elif request.method == "DELETE" or request.method == "PUT" or request.method == "PATCH":
            return bool(request.user and  request.user == obj.author)
        else:
            return bool(request.user and request.user.is_authenticated)

        
class IsUserAccount(permissions.BasePermission):
   
    """This permission prevent users to delete their account. Accounts can only be deleted 
    by the super user. 
    Users can however modified their data if needed.
    """

    def has_object_permission(self, request, view, obj):

        if request.method == "GET":
            return bool(request.user and  request.user.id == obj.id or request.user.is_superuser)
        elif request.method == "DELETE" :
            return bool(request.user and  request.user.is_superuser)
        elif request.method == "PUT" or request.method == "PATCH":
            return bool(request.user and  request.user.id == obj.id)
        else:
            return bool(request.user and request.user.is_authenticated)
    