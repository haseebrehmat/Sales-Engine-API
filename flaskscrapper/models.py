from django.db import models
from utils.model_fields.timestamped import TimeStamped


class ScraperRunningStatus(TimeStamped):
    job_source = models.CharField(max_length=250, blank=True, null=True)
    status = models.BooleanField(default=False)

class ScrapersLoopStatus(TimeStamped):
    job_source = models.CharField(max_length=250, blank=True, null=True)
    loop_status = models.BooleanField(default=False)