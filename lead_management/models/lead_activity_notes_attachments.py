from django.db import models

from settings.utils.model_fields import TimeStamped
from .lead_activity_notes import LeadActivityNotes


class LeadActivityNotesAttachment(TimeStamped):
    lead_activity_notes = models.ForeignKey(LeadActivityNotes, on_delete=models.SET_NULL, blank=True, null=True)
    attachment = models.TextField(blank=True, null=True)
    filename = models.CharField(max_length=256, blank=True)

    class Meta:
        default_permissions = ()
        db_table = "lead_activity_notes_attachments"

    def __str__(self):
        return self.attachment
