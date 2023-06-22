from django.db import models

from authentication.models import User
from authentication.models.company import Company
from candidate.models.candidate import Candidate
from utils.model_fields.timestamped import TimeStamped


class CandidateLogs(TimeStamped):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name="candidate_company")
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    exposed_user = models.ForeignKey(Candidate, on_delete=models.SET_NULL, blank=True, null=True)
    exposed_to = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="candidate_exposed_to")
    def __str__(self):
        return f"{self.company.name} - {self.exposed_user.name}"

