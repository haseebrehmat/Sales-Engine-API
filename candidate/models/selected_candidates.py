from django.db import models

from authentication.models.company import Company
from candidate.models.candidate import Candidate
from utils.model_fields.timestamped import TimeStamped


class SelectedCandidate(TimeStamped):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.candidate.name} - {self.company.name}'

    class Meta:
        unique_together = ("company", "candidate")
