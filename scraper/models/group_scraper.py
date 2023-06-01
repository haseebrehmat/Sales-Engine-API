from django.db import models

from scraper.models.scheduler_settings import SchedulerSettings
from utils.model_fields.timestamped import TimeStamped


class GroupScraper(TimeStamped):
    name = models.CharField(max_length=50, null=True, unique=True)
    scheduler_settings = models.ForeignKey(
        SchedulerSettings, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
