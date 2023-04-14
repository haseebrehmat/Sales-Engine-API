import os
import subprocess
from job_scraper.utils.thread import start_new_thread
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
import django
from settings.base import ENVIRONMENT

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.{ENVIRONMENT}')
django.setup()
from job_scraper.models import SchedulerSettings
from job_scraper.utils.helpers import convert_time_into_minutes

objects = SchedulerSettings.objects.all()

app = Celery('settings')

app.config_from_object('django.conf:settings', namespace='CELERY')
scheduler_config = {}

for object in objects:
    scheduler_config[f'{object.job_source}'] = {
        'task': 'job_scraper.schedulers.job_upload_scheduler.load_job_scrappers',
        'schedule': None,
        'args': [object.job_source],
    }
    if object.interval_based:
        interval_mins = convert_time_into_minutes(object.interval, object.interval_type)
        scheduler_config[object.job_source]['schedule'] = timedelta(minutes=interval_mins)
    else:
        hour = object.time.hour
        min = object.time.minute
        scheduler_config[object.job_source]['schedule'] = crontab(minute=min, hour=hour)

app.conf.beat_schedule = scheduler_config
app.conf.timezone = 'Asia/Karachi'
app.autodiscover_tasks()


@start_new_thread
def restart_server():                               # New Function for Restart Beat
    pid = None
    cmd = 'celery -A settings beat -l info'
    for line in os.popen('ps aux | grep "%s" | grep -v grep' % cmd):
        fields = line.strip().split()
        pid = fields[1]
    if pid:
        subprocess.run(['kill', pid])
    subprocess.run(['celery', '-A', 'settings', 'beat', '-l', 'info'])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
