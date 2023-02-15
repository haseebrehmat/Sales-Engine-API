import uuid

from django.db import models
from authentication.models import User
from settings.utils.model_fields import TimeStamped


class Profile(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    employee_id = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.first_name} - {self.employee_id}"

    class Meta:
        unique_together = ("company", "employee_id")
