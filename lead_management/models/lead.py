import uuid
from django.db import models
from candidate.models import Candidate
from job_portal.models import AppliedJobStatus
from lead_management.models.company_status import CompanyStatus
from lead_management.models.phase import Phase
from settings.utils.model_fields import TimeStamped
from authentication.models import User


class Lead(TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    applied_job_status = models.OneToOneField(AppliedJobStatus, on_delete=models.SET_NULL, null=True)
    company_status = models.ForeignKey(CompanyStatus, on_delete=models.SET_NULL, null=True)
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True)
    converter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    edited = models.BooleanField(default=False)

    class Meta:
        default_permissions = ()
        db_table = "lead"

    def __str__(self):
        return self.applied_job_status.job.job_title if self.applied_job_status and self.applied_job_status.job else ''
