from django.contrib import admin

from job_portal.models import AppliedJobStatus, JobDetail

# Register your models here.

admin.site.register(JobDetail)
admin.site.register(AppliedJobStatus)