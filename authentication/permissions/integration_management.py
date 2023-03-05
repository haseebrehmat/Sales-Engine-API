from rest_framework.permissions import BasePermission
from utils.helpers import validate_request


class IntegrationPermissions(BasePermission):
    message = "You don't have access to this endpoint!"

    def has_permission(self, request, view):
        permissions = {
            'GET': ['view_integration'],
            'POST': ['create_integration'],
            'PUT': ['edit_integration'],
            'DELETE': ['delete_integration']
        }
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return validate_request(request, permissions)
        else:
            return False

