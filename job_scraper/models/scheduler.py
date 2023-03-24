from django.db import models
from utils.model_fields.timestamped import TimeStamped


class SchedulerSync(TimeStamped):
    running = models.BooleanField(default=False)
