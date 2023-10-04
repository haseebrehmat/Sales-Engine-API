from settings.base import env

try:
    import os
    import shutil
    from scraper.models import SchedulerSync, AllSyncConfig
    SchedulerSync.objects.filter(type='instant').update(running=False, uploading=False)
    SchedulerSync.objects.filter(type='group scraper').update(uploading=False)
    AllSyncConfig.objects.filter(status=True).update(status=False)

    if os.path.exists('scraper/job_data'):
        shutil.rmtree('scraper/job_data')
        os.makedirs('scraper/job_data')
        pass
    else:
        os.makedirs('scraper/job_data')
except Exception as e:
    print("Error in job_upload_scheduler init - file", str(e))
