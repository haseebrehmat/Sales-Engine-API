from django.db import models

from authentication.models.company import Company
from candidate.models.designation import Designation
from utils.model_fields.timestamped import TimeStamped


class Candidate(TimeStamped):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    employee_id = models.CharField(max_length=100, blank=True, null=True, )
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    experience = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, blank=True, null=True)




