from django.db import models

from utils.model_fields.timestamped import TimeStamped


class JobSourceQuery(TimeStamped):
    job_source = models.CharField(max_length=100, unique=True)
    queries = models.JSONField()