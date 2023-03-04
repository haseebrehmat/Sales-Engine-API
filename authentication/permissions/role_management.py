from rest_framework.permissions import BasePermission
from utils.helpers import validate_request


class RolePermissions(BasePermission):
    message = "You don't have access to this endpoint!"

    def has_permission(self, request, view):
        permissions = {
            'GET': ['view_role'],
            'POST': ['create_role'],
            'PUT': ['edit_role'],
            'DELETE': ['delete_role']
        }
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return validate_request(request, permissions)
        else:
            return False

