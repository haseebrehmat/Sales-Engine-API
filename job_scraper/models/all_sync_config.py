from django.db import models

from utils.model_fields.timestamped import TimeStamped


class AllSyncConfig(TimeStamped):
    status = models.BooleanField(default=False)
