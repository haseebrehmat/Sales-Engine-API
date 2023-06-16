from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from utils.model_fields.timestamped import TimeStamped


class Tools(TimeStamped):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.name


class CandidateTools(TimeStamped):
    candidate = models.ForeignKey('Candidate', on_delete=models.SET_NULL, blank=True, null=True)
    tool = models.ForeignKey('Tools', on_delete=models.CASCADE, blank=True, null=True)
    experience_level = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return f"{self.candidate.name} - {self.tool.name}"

