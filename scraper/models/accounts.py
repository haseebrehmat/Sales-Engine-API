from django.db import models

from scraper.utils.custom_validators import source_validator
from utils.model_fields.timestamped import TimeStamped


class Accounts(TimeStamped):
    email = models.CharField(max_length=500, blank=False, null=False)
    password = models.CharField(max_length=200, blank=False, null=False)
    source = models.CharField(max_length=200, null=True, blank=True, validators=[source_validator])

    class Meta:
        unique_together = ('email', 'source')

    def __str__(self):
        return f"{self.email} {self.source}"
