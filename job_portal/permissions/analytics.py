from rest_framework.permissions import BasePermission

from utils.helpers import validate_request


class AnalyticsPermission(BasePermission):
    message = "You don't have access to this endpoint!"

    def has_permission(self, request, view):
        permissions = {
            'GET': ["view_analytics"],
        }
        # if not request.user.is_superuser:
        #     return True
        if request.user.is_authenticated:
            return validate_request(request, permissions)
        else:
            return False
