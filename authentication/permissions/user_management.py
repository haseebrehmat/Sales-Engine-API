from rest_framework.permissions import BasePermission
from utils.helpers import validate_request


class UserPermissions(BasePermission):
    message = "You don't have access to this endpoint!"

    def has_permission(self, request, view):
        print(request.user.is_authenticated)

        permissions = {
            'GET': ['view_team','view_user'],
            'POST': ['create_team'],
            'PUT': ['edit_team', 'change_user_status'],
            'DELETE': ['delete_team']
        }
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return validate_request(request, permissions)
        else:
            return False

