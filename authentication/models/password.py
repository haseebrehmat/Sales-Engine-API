import uuid

from django.db import models
from authentication.models import User
from settings.utils.model_fields import TimeStamped


class PasswordChangeLogs(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=200)


class ResetPassword(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_code = models.CharField(max_length=10)
    status = models.BooleanField(default=False)


