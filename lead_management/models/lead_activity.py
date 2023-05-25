from django.db import models

from candidate.models import Candidate
from settings.utils.model_fields import TimeStamped
from .company_status import CompanyStatus
from .lead import Lead
from .phase import Phase


class LeadActivity(TimeStamped):
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True)
    company_status = models.ForeignKey(
        CompanyStatus, on_delete=models.SET_NULL, null=True)
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True)
    effect_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(auto_now_add=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('lead', 'company_status', 'phase', 'candidate')
        default_permissions = ()
        db_table = "lead_activity"

    def __str__(self):
        return f'{self.lead} - {self.company_status} - {self.phase}'
