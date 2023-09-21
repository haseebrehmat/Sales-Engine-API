from django.db import models
from utils.model_fields.timestamped import TimeStamped


class JobSource(TimeStamped):
    name = models.CharField(max_length=200, blank=True, null=True)
    key = models.CharField(max_length=200, blank=False, null=False, unique=True)
    def __str__(self):
        return f"{self.name}"
