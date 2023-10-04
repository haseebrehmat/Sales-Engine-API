import datetime
from django.utils import timezone
from settings.utils.model_fields import TimeStamped
from django.db import models


class ScraperLogs(TimeStamped):
    job_source = models.CharField(max_length=250, default="")
    total_jobs = models.IntegerField(default=0)
    filename = models.CharField(max_length=1000, default="")
    uploaded_jobs = models.IntegerField(default=0)


