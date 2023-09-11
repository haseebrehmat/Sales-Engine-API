from django.db import models
from scraper.models.group_scraper import GroupScraper
from utils.model_fields.timestamped import TimeStamped


class GroupScraperQuery(TimeStamped):
    group_scraper = models.ForeignKey(GroupScraper, on_delete=models.SET_NULL, blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    job_type = models.CharField(max_length=250, blank=True, null=True)
    job_source = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(default="remaining", max_length=250)
    end_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    start_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.group_scraper.name} - {self.job_source} - {self.job_type}"
