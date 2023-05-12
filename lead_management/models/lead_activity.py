from django.db import models

from settings.utils.model_fields import TimeStamped
from .company_status import CompanyStatus
from .lead import Lead
from .phase import Phase


class LeadActivity(TimeStamped):
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    company_status = models.ForeignKey(CompanyStatus, on_delete=models.SET_NULL, blank=True, null=True)
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        default_permissions = ()
        db_table = "lead_activity"

    def __str__(self):
        return self.name
