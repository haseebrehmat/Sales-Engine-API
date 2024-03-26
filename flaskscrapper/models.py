from django.db import models
from utils.model_fields.timestamped import TimeStamped


class ScrapersRunningStatus(TimeStamped):
    job_source = models.CharField(max_length=250, blank=True, null=True)
    running = models.BooleanField(default=False)
    loop = models.BooleanField(default=False)
