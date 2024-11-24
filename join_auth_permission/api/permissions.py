from rest_framework import permissions


class IsOwnerOrReadOnlyIfAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):

        if request.method == 'GET':
            return bool(request.user and (request.user.is_superuser or request.user.id == obj.id) )
        else:
            return bool(request.user and request.user.id == obj.id)
