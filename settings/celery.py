import os
import subprocess
import time

import django
from celery import Celery
from celery import shared_task
from django.utils import timezone

from scraper.utils.thread import start_new_thread
from settings.base import ENVIRONMENT, env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.{ENVIRONMENT}')
django.setup()

from celery.schedules import timedelta

app = Celery('settings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'check_group_scraper': {
        'task': 'settings.celery.check_group_scraper',
        'schedule': timedelta(seconds=1500),
    },
    'octagon_scraper_bot': {
        'task': 'settings.celery.octagon_scraper_bot',
        'schedule': timedelta(seconds=10800),
    }
}

app.conf.timezone = 'Asia/Karachi'
app.autodiscover_tasks()

from scraper.models.scheduler import SchedulerSync
from scraper.models import ScraperLogs
from scraper.management.commands.check_scraper import check_current_group

SchedulerSync.objects.all().update(running=False)

@shared_task
def check_group_scraper():
    group_scrapper = check_current_group()
    check_status = SchedulerSync.objects.filter(
        type="group scraper", job_source=group_scrapper.name.lower()).first()
    if not check_status.running and group_scrapper.scheduler_settings.time_based:
        os.system('pgrep chrome | xargs kill -9')
        time.sleep(10)
        restart_script()
    elif not int((timezone.now() - ScraperLogs.objects.all().last().updated_at).total_seconds()/60) < 30:
        os.system('pgrep chrome | xargs kill -9')
        time.sleep(10)
        restart_script()
    else:
        print("")

@start_new_thread
def restart_script():
    try:
        pid = None
        cmd = 'python manage.py check_scraper'
        for line in os.popen('ps aux | grep "%s" | grep -v grep' % cmd):
            fields = line.strip().split()
            pid = fields[1]
        if pid:
            subprocess.run(['kill', pid])
        subprocess.run(['python', 'manage.py', 'check_scraper'])
    except:
        print("")

@shared_task
def octagon_scraper_bot():
    try:
        from utils.octagon_slack_bot import notify_octagon_scraper_stats_via_slack
        if env('ENVIRONMENT') == 'production':
            notify_octagon_scraper_stats_via_slack()
    except Exception as e:
        print(e)

