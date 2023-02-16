from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class InvalidFileException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('File not supported.')
    default_code = 'error'

class NotAuthorized(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('File not supported.')
    default_code = 'error'

class NoActiveUserException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('No active user found')
    default_code = 'error'
