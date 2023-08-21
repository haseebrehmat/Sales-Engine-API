from django.db import models
from django.contrib.postgres.fields import ArrayField
from authentication.models.company import Company
from candidate.models.exposed_candidates import ExposedCandidate
from utils.model_fields import TimeStamped


class CandidateTeam(TimeStamped):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=False, null=False, default="Nothing")
    exposed_to = ArrayField(models.CharField(max_length=300), blank=True, null=True)
    def __str__(self):
        return f"{self.name} - {self.company.name}"
    class Meta:
        unique_together = ('company', 'name')
class ExposedCandidateTeam(TimeStamped):
    candidate_team = models.ForeignKey(CandidateTeam, on_delete=models.CASCADE, blank=True, null=True)
    exposed_candidate = models.ForeignKey(ExposedCandidate, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"{self.candidate_team.name} - {self.exposed_candidate.candidate.name}"
    class Meta:
        unique_together = ('candidate_team', 'exposed_candidate')
