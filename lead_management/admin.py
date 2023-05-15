from django.contrib import admin

from lead_management.models import Status, CompanyStatus, Phase, Lead, LeadActivity, LeadActivityNotes

# Register your models here.
admin.site.register(Status)
admin.site.register(CompanyStatus)
admin.site.register(Phase)
admin.site.register(Lead)
admin.site.register(LeadActivity)
admin.site.register(LeadActivityNotes)
