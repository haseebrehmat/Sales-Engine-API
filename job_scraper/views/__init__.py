import os
from job_scraper.models import AllSyncConfig
# from job_scraper.models import SchedulerSync
# from job_scraper.schedulers.job_upload_scheduler import upload_jobs, remove_files
#
# upload_jobs()
# remove_files(job_source="all")
# SchedulerSync.objects.all().update(running=False)
AllSyncConfig.objects.all().update(status=False)
if not os.path.exists('job_scraper/job_data'):
    os.makedirs('job_scraper/job_data')
