try:
    import os
    from scraper.models import AllSyncConfig
    from scraper.models import SchedulerSync
    # from scraper.schedulers.job_upload_scheduler import upload_jobs, remove_files
    #
    # upload_jobs()
    # remove_files(job_source="all")
    SchedulerSync.objects.all().update(running=False)
    AllSyncConfig.objects.all().update(status=False)
    if not os.path.exists('scraper/job_data'):
        os.makedirs('scraper/job_data')
except Exception as e:
    print("Error in job_upload_scheduler init - file", str(e))
