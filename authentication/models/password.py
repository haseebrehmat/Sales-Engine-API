from django.db import models
from authentication.models import User
from settings.utils.model_fields import TimeStamped


class PasswordChangeLogs(TimeStamped):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=200)


class ResetPassword(TimeStamped):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_code = models.CharField(max_length=10)
    status = models.BooleanField(default=False)


