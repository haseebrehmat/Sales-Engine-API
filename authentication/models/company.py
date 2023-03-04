import uuid
from django.db import models

from utils.company_api_enums import API_CHOICES
from settings.utils.model_fields import TimeStamped


class Company(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=500)
    code = models.CharField(max_length=500, blank=True, unique=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}__{self.code}"

    class Meta:
        default_permissions = ()
        permissions = (
            ("create_company", "create company"),
            ("view_company", "view company"),
            ("update_company", "update company"),
            ("delete_company", "delete company"),
        )
        ordering = ['-created_at']
        db_table = "company"


class CompanyAPIIntegration(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, blank=True, null=True, choices=API_CHOICES)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    api_key = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company.name} - {self.name}"

    class Meta:
        default_permissions = ()
        db_table = "company_api_integration"
