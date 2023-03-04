from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class InvalidUserException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _('User not found.')
    default_code = 'error'
