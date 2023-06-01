from django.db import models
from scraper.models.group_scraper import GroupScraper
from utils.model_fields.timestamped import TimeStamped


class GroupScraperQuery(TimeStamped):
    group_scraper = models.OneToOneField(GroupScraper, on_delete=models.SET_NULL, blank=True, null=True)
    queries = models.JSONField()
