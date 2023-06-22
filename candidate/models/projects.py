from django.db import models
from django.contrib.postgres.fields import ArrayField
from utils.model_fields.timestamped import TimeStamped

class CandidateProjects(TimeStamped):
    candidate = models.ForeignKey('Candidate', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, null=False, default="N/A")
    description = models.TextField(null=True, blank=True)
    tags = ArrayField(models.CharField(max_length=300), blank=True, null=True)

    def __str__(self):
        if self.candidate is not None and self.name is not None:
            return f"{self.candidate.name} - {self.name}"
        elif self.candidate is not None:
            return f"{self.candidate.name} - Unassigned"
        else:
            return f"Unassigned - {self.name}"
    class Meta:
        unique_together = ("name", "candidate")

# class ProjectImage(TimeStamped):
#     project = models.ForeignKey('CandidateProjects', on_delete=models.SET_NULL, blank=True, null=True)
#     image = models.TextField(null=True, blank=True)
#     def __str__(self):
#         return f'{self.project.name} - {self.image}'