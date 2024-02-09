from django.db import models
from scraper.models.scheduler_settings import SchedulerSettings
from utils.model_fields.timestamped import TimeStamped


class GroupScraper(TimeStamped):
    scheduler_settings = models.ForeignKey(
        SchedulerSettings, on_delete=models.SET_NULL, blank=True, null=True)
    running_link = models.ForeignKey('GroupScraperQuery', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=50, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    disabled = models.BooleanField(default=False)
    is_analytics = models.BooleanField(default=False)
    running_start_time = models.DateTimeField(blank=True, null=True)


