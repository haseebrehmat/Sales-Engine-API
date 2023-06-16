from django.core.exceptions import ValidationError
from django.db import models

from authentication.models.company import Company
from utils.model_fields import TimeStamped


class Designation(TimeStamped):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.company.name} - {self.title}"

    class Meta:
        unique_together = ('company', 'title')


