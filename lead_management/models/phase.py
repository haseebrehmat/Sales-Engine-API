from django.db import models

from .company_status import CompanyStatus


class Phase(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    company_status = models.ForeignKey(CompanyStatus, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        default_permissions = ()
        db_table = "phase"

    def __str__(self):
        return self.name
