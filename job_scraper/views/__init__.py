from job_scraper.models import SchedulerSync
from job_scraper.schedulers.job_upload_scheduler import upload_jobs, remove_files

upload_jobs()
remove_files(job_source="all")
SchedulerSync.objects.all().update(running=False)