from authentication.models.company import Company
from utils.model_fields.timestamped import TimeStamped
from django.db import models


class Pseudos(TimeStamped):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=250)

