from django.db import models
from utils.model_fields.timestamped import TimeStamped


class SchedulerSync(TimeStamped):
    job_source = models.CharField(max_length=200, blank=True, null=True)
    running = models.BooleanField(default=False)
    type = models.CharField(default="instant", max_length=250)
    start_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    end_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    uploading = models.BooleanField(default=False)

    class Meta:
        unique_together = ["job_source", "type"]
    def __str__(self):
        return f"{self.job_source} - {self.type}"
