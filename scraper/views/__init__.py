from scraper.schedulers.job_upload_scheduler import group_scraper_job, load_all_job_scrappers
from settings.base import env
from utils.octagon_slack_bot import notify_octagon_scraper_stats_via_slack

try:
    import os
    import shutil
    from scraper.models import SchedulerSync, AllSyncConfig
    SchedulerSync.objects.filter(type='instant').update(running=False, uploading=False)
    SchedulerSync.objects.filter(type='group scraper').update(uploading=False)
    AllSyncConfig.objects.filter(status=True).update(status=False)
    # if env('ENVIRONMENT') == 'production':
    #     notify_octagon_scraper_stats_via_slack()

    # if env("ENVIRONMENT") == "development":
    #     AllSyncConfig.objects.filter(status=False).update(status=True)
    #     SchedulerSync.objects.filter(type='infinte_scraper').update(running=False, uploading=False)
    #     print("Linkedin group scraper init --")
    #     load_all_job_scrappers()

    if os.path.exists('scraper/job_data'):
        shutil.rmtree('scraper/job_data')
        os.makedirs('scraper/job_data')
        pass
    else:
        os.makedirs('scraper/job_data')
    # group_scraper_job("4")
except Exception as e:
    print("Error in job_upload_scheduler init - file", str(e))
