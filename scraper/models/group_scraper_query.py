from django.db import models
from utils.model_fields.timestamped import TimeStamped


class GroupScraperQuery(TimeStamped):
    group_scraper = models.ForeignKey('GroupScraper', on_delete=models.SET_NULL, blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    job_type = models.CharField(max_length=250, blank=True, null=True)
    job_source = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(default="remaining", max_length=250)
    preference = models.PositiveIntegerField(default=1)
    end_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if self.group_scraper is not None:
            return f"{self.group_scraper.name} - {self.job_source} - {self.job_type}"
        else:
            return f"Unassigned - {self.job_source} - {self.job_type}"

        