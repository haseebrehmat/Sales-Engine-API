from django.db import models
from authentication.models import User
import uuid

# Create your models here.
class Log(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True)

    level = models.CharField(max_length=10)
    log_message = models.TextField(null=True)
    error_message = models.TextField(null=True)
    error_line=models.TextField(null=True)
    traceback = models.TextField(null=True)
    path = models.CharField(max_length=1000,null=True)
    line_number = models.IntegerField(null=True)
    method = models.CharField(max_length=10,null=True)
    status_code = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
