
from pprint import pprint
from rest_framework import permissions


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            # this call is needed for request permissions
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator

class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff and request.user.is_superuser)

class IsOwnUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user 
            and request.user.is_authenticated
            and request.user.id == view.kwargs["id"]) or bool(
                request.user and request.user.is_staff)