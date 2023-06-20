from rest_framework.permissions import BasePermission

from utils.helpers import validate_request


class GenericSkillsPermissions(BasePermission):
    message = "You don't have access to this endpoint!"

    def has_permission(self, request, view):
        permissions = {
            'GET': ['view_generic_skill'],
            'POST': ['create_generic_skill'],
            'PUT': ['edit_generic_skill'],
            'DELETE': ['delete_generic_skill']
        }
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return validate_request(request, permissions)
        else:
            return False
