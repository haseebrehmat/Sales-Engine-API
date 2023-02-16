from django.contrib import admin

from job_portal.models import AppliedJobStatus, JobDetail

# Register your models here.

# class JobDetailAdmin(admin.ModelAdmin):
#     list_display = ('job_title', 'company_name', 'job_source', 'job_posted_date','job_status')

# admin.site.register(JobDetail,JobDetailAdmin)
admin.site.register(AppliedJobStatus)