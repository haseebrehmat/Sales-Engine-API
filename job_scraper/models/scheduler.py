from django.db import models
from utils.model_fields.timestamped import TimeStamped


class SchedulerSync(TimeStamped):
    job_source = models.CharField(max_length=200, blank=True, null=True)
    running = models.BooleanField(default=False)
    type = models.CharField(default="instant", max_length=250)

    class Meta:
        unique_together = ["job_source", "type"]
