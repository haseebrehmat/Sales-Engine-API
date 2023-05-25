from rest_framework.permissions import BasePermission

from utils.helpers import validate_request


class VerticalPermissions(BasePermission):
    message = "You don't have access to this endpoint!"

    def has_permission(self, request, view):
        permissions = {
            'GET': ['edit_vertical'],
            'POST': ['create_vertical'],
            'PUT': ['edit_vertical'],
            'DELETE': ['delete_vertical']
        }
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return validate_request(request, permissions)
        else:
            return False
