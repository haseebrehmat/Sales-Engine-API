from django.db import models
from utils.model_fields.timestamped import TimeStamped


class SchedulerSync(TimeStamped):
    job_source = models.CharField(unique=True, max_length=200, blank=True, null=True)
    running = models.BooleanField(default=False)
