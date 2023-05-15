from django.db import models

from authentication.models import User
from settings.utils.model_fields import TimeStamped
from .lead_activity import LeadActivity


class LeadActivityNotes(TimeStamped):
    lead_activity = models.ForeignKey(LeadActivity, on_delete=models.SET_NULL, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        default_permissions = ()
        db_table = "lead_activity_notes"

    def __str__(self):
        return self.message
