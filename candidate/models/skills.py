from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from utils.model_fields.timestamped import TimeStamped


class Skills(TimeStamped):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CandidateSkills(TimeStamped):
    candidate = models.ForeignKey('Candidate', on_delete=models.SET_NULL, blank=True, null=True)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    level = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        if self.candidate is not None and self.skill is not None:
            return f"{self.candidate.name} - {self.skill.name}"
        elif self.candidate is not None:
            return f"{self.candidate.name} - Unassigned"
        else:
            return f"Unassigned - {self.skill.name}"
