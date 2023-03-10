from rest_framework.permissions import BasePermission

from utils.helpers import validate_request


class ApplyJobPermission(BasePermission):
    message = "You don't have access to this endpoint!"
    def has_permission(self, request, view):
        permissions = {
            'GET': None,
            'PATCH': ['change_job_status'],
            'POST': ['apply_job'],
            'PUT': None,
            'DELETE': None
        }
        # if not request.user.is_superuser:
        #     return True
        print("jasdlfjsadlf",request.method)
        if request.user.is_authenticated:
            return validate_request(request, permissions)
        else:
            return False
