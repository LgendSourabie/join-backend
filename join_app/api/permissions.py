from rest_framework import permissions

class IsAuthenticatedOrNot(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        is_author = bool(request.user and request.user == obj.author)
        return is_author or request.method in permissions.SAFE_METHODS
