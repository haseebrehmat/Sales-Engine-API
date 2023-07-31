from settings.base import env

try:
    import os
    import shutil
    from scraper.models import SchedulerSync
    # from scraper.views.sync_scheduler import run_scrapers_manually
    SchedulerSync.objects.all().update(running=False)
    # if AllSyncConfig.objects.filter(status=True).exists():
    #     run_scrapers_manually()
    if os.path.exists('scraper/job_data'):
        shutil.rmtree('scraper/job_data')
        os.makedirs('scraper/job_data')
        pass
    else:
        os.makedirs('scraper/job_data')
except Exception as e:
    print("Error in job_upload_scheduler init - file", str(e))
