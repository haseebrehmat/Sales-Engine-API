from django.db import models

from authentication.models.company import Company
from candidate.models.candidate import Candidate
from utils.model_fields.timestamped import TimeStamped


class ExposedCandidate(TimeStamped):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    allowed_status = models.BooleanField(default=True)

    class Meta:
        db_table = "exposed_candidates"
        unique_together = ("candidate", "company")
        default_permissions = ()

    def __str__(self):
        return f'{self.candidate} - {self.company}'

