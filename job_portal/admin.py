from django.contrib import admin

from job_portal.models import AppliedJobStatus, JobDetail, BlacklistJobs, EditHistory, SalesEngineJobsStats, JobArchive


# Register your models here.

class JobDetailAdmin(admin.ModelAdmin):
    list_display = ('job_title','tech_keywords', 'company_name', 'job_source', 'job_posted_date')
    list_filter = ('tech_keywords','company_name',)

class AppliedJobAdmin(admin.ModelAdmin):
    list_display = ('applied_by', 'applied_date','job_status',)
    list_filter = ('applied_by','job_status','applied_date',)


admin.site.register(JobDetail, JobDetailAdmin)
admin.site.register(AppliedJobStatus, AppliedJobAdmin)
admin.site.register(BlacklistJobs)
admin.site.register(EditHistory)
admin.site.register(SalesEngineJobsStats)
admin.site.register(JobArchive)
