from django.db import models

from utils.model_fields.timestamped import TimeStamped


class RestrictedJobsTags(TimeStamped):
    tag = models.CharField(max_length=100, blank=True, null=True, unique=True)

