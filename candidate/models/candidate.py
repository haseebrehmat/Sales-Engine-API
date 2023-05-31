from django.db import models

from authentication.models.company import Company
from candidate.models.designation import Designation
from utils.model_fields.timestamped import TimeStamped


class Candidate(TimeStamped): # company // all
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    employee_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30)
    experience = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=100)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.company.name}"




