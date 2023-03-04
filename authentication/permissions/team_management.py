from rest_framework.permissions import BasePermission
from utils.helpers import validate_request


class TeamPermissions(BasePermission):
    message = "You don't have access to this endpoint!"

    def has_permission(self, request, view):
        permissions = {
            'GET': ['view_team'],
            'POST': ['create_team'],
            'PUT': ['edit_team'],
            'DELETE': ['delete_team']
        }
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return validate_request(request, permissions)
        else:
            return False

