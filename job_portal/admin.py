from django.contrib import admin

from job_portal.models import AppliedJobStatus, JobDetail, BlacklistJobs


# Register your models here.

class JobDetailAdmin(admin.ModelAdmin):
    list_display = ('job_title','tech_keywords', 'company_name', 'job_source', 'job_posted_date', 'job_status')
    list_filter = ('tech_keywords','company_name',)


admin.site.register(JobDetail, JobDetailAdmin)
admin.site.register([AppliedJobStatus, BlacklistJobs])
