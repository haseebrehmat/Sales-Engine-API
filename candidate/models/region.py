from django.db import models

from utils.model_fields.timestamped import TimeStamped


class Regions(TimeStamped):
    region = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.region

class CandidateRegions(TimeStamped):
    candidate = models.ForeignKey('Candidate', on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey('Regions', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        if self.candidate is not None and self.region is not None:
            return f"{self.candidate.name} - {self.region.region}"
        elif self.candidate is not None:
            return f"{self.candidate.name} - Unassigned"
        else:
            return f"Unassigned - {self.region.region}"
        # return f"{self.candidate.name} - {self.region.region}"

