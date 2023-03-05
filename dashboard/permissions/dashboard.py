from rest_framework.permissions import BasePermission
from utils.helpers import validate_request


class DashboardPermission(BasePermission):
    message = "You don't have access to this endpoint!"
    def has_permission(self, request, view):
        permissions = {
            'GET': ['view_dashboard'],
            'POST': None,
            'PUT': None,
            'DELETE': None,
            'PATCH': None
        }
        # for super user
        if not request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return validate_request(request, permissions)
        else:
            return False