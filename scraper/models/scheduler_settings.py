import uuid

from django.db import models

from utils.model_fields.timestamped import TimeStamped


class SchedulerSettings(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    time_based = models.BooleanField(default=False)
    interval_based = models.BooleanField(default=False)
    time = models.TimeField(null=True)
    interval = models.IntegerField(default=0, null=True, blank=True)
    interval_type = models.CharField(max_length=100, null=True, blank=True)
    job_source = models.CharField(max_length=100, null=False, blank=False, default='')
    week_days = models.CharField(max_length=256, null=False, blank=True, default='')
    is_group = models.BooleanField(default=False)

    class Meta:
        default_permissions = ()
