from django.db import models

from authentication.models.company import Company
from .status import Status


class CompanyStatus(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(
        Status, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('company', 'status',)
        default_permissions = ()
        db_table = "company_status"

    def __str__(self):
        return self.status.name
