import uuid

from django.db import models

from pseudos.models import Verticals
from settings.utils.model_fields import TimeStamped


class Profile(TimeStamped):
    vertical = models.ManyToManyField(Verticals, related_name='vertical', blank=True)

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    is_restricted = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    employee_id = models.CharField(max_length=100, blank=True, null=True, )
    file_url = models.TextField(blank=True, null=True)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        db_table = "profile"
        unique_together = ("company", "employee_id")
        default_permissions = ()
