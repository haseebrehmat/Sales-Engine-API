import subprocess
from scraper.utils.thread import start_new_thread
from celery import Celery
import django
from settings.base import ENVIRONMENT
from celery import shared_task
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.{ENVIRONMENT}')
django.setup()

from celery.schedules import timedelta

app = Celery('settings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'check_group_scraper': {
        'task': 'settings.celery.check_group_scraper',
        'schedule': timedelta(seconds=600),
    }
}

app.conf.timezone = 'Asia/Karachi'
app.autodiscover_tasks()

from scraper.models.scheduler import SchedulerSync
from scraper.management.commands.check_scraper import check_current_group

SchedulerSync.objects.all().update(running=False)
@shared_task
def check_group_scraper():
    group_scrapper = check_current_group()
    check_status = SchedulerSync.objects.filter(
        type="group scraper", job_source=group_scrapper.name.lower()).first()
    # print(f"This is the time of {group_scrapper.name}")
    if not check_status.running and group_scrapper.scheduler_settings.time_based:
        # print("Group is stopped and celery start group scrapper again")
        restart_script()
    else:
        print("")
        # print("Group is running already")
@start_new_thread
def restart_script():
    pid = None
    cmd = 'python manage.py check_scraper'
    for line in os.popen('ps aux | grep "%s" | grep -v grep' % cmd):
        fields = line.strip().split()
        pid = fields[1]
    if pid:
        subprocess.run(['kill', pid])
    subprocess.run(['python', 'manage.py', 'check_scraper'])
