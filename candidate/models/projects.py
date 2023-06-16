from django.db import models

from utils.model_fields.timestamped import TimeStamped

class CandidateProjects(TimeStamped):
    candidate = models.ForeignKey('Candidate', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class ProjectImage(TimeStamped):
    project = models.ForeignKey('CandidateProjects', on_delete=models.SET_NULL, blank=True, null=True)
    image = models.TextField(null=True, blank=True)
    def __str__(self):
        return f'{self.project.name} - {self.image}'