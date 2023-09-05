import time
import subprocess
from scraper.utils.thread import start_new_thread
# from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
import django
from datetime import datetime, time
from settings.base import ENVIRONMENT
from celery import shared_task
import os
from celery.signals import task_received
from django.dispatch import receiver



os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.{ENVIRONMENT}')
django.setup()

from celery.schedules import timedelta

app = Celery('settings')

# Configure Celery using Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')



# Define the schedule for the task
app.conf.beat_schedule = {
    'check_group_scraper': {
        'task': 'settings.celery.check_group_scraper',
        'schedule': timedelta(seconds=600),
    }
}

# Set the timezone
app.conf.timezone = 'Asia/Karachi'

# Autodiscover and register tasks
app.autodiscover_tasks()

from scraper.models.scheduler import SchedulerSync
from scraper.management.commands.check_scraper import check_current_group

SchedulerSync.objects.all().update(running=False)
@shared_task
def check_group_scraper():
    group_scrapper = check_current_group()
    check_status = SchedulerSync.objects.filter(
        type="group scraper", job_source=group_scrapper.name.lower()).first()
    if not check_status.running and group_scrapper.scheduler_settings.time_based:
        restart_script()
    else:
        print("")

@start_new_thread
def restart_script():                               # New Function for Restart Beat
    pid = None
    cmd = 'python manage.py check_scraper'
    for line in os.popen('ps aux | grep "%s" | grep -v grep' % cmd):
        fields = line.strip().split()
        pid = fields[1]
    if pid:
        subprocess.run(['kill', pid])
    subprocess.run(['python', 'manage.py', 'check_scraper'])
# for backup previous code
# from scraper.models import SchedulerSettings
# from scraper.models.celery_source import CeleryModel
# from scraper.utils.helpers import convert_time_into_minutes
#from scraper.schedulers.job_upload_scheduler import check_group_scraper
# objects = SchedulerSettings.objects.all()
# app = Celery('settings')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# scheduler_config = {}
#
# for object in objects:
#     scheduler_config[f'{object.job_source}'] = {
#         # 'task': 'scraper.schedulers.job_upload_scheduler.run_scraper_by_celery',
#         'task': f'settings.celery.{object.job_source}',
#         'schedule': None,
#         # 'args': [object.job_source],
#     }
#     if object.interval_based:
#         interval_mins = convert_time_into_minutes(object.interval, object.interval_type)
#         scheduler_config[object.job_source]['schedule'] = timedelta(minutes=interval_mins)
#     else:
#         hour = object.time.hour
#         min = object.time.minute
#         scheduler_config[object.job_source]['schedule'] = crontab(minute=min, hour=hour)
# app.conf.beat_schedule = scheduler_config
# app.conf.beat_schedule = {
#     'celery_task': {
#         'task': 'check_group_scrapper',
#         'schedule': 2.0,
#     }
# }
# app.conf.timezone = 'Asia/Karachi'
# app.autodiscover_tasks()

# @shared_task(bind=True)
# def jooble(self):
#     # obj = CeleryModel.objects.filter(name='jooble').first()
#     # print(f"Session state of Jooble before set : "
#     #       f"{obj.status}")
#     # obj.status = True
#     # obj.save()
#     # print(f"Session state of Jooble after set : "
#     #       f"{obj.status}")
#     current_time = datetime.datetime.now()
#     formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
#     original_time = datetime.datetime.strptime(formatted_time, "%Y-%m-%d %H:%M:%S")
#     # Add 2 minutes to the original_time
#     new_time = original_time + datetime.timedelta(minutes=2)
#     # while CeleryModel.objects.filter(name='jooble').first().status:
#     while datetime.datetime.now() <= new_time:
#         print(f'Task jooble is running...')
#         time.sleep(5)  # Simulate task work
# @shared_task(bind=True)
# def himalayas(self):
#     # obj = CeleryModel.objects.filter(name='himalayas').first()
#     # print(f"Session state of himalayas before set : "
#     #       f"{obj.status}")
#     # obj.status = True
#     # obj.save()
#     # print(f"Session state of himalayas after set : "
#     #       f"{obj.status}")
#     while CeleryModel.objects.filter(name='himalayas').first().status:
#         print(f'Task himalayas is running...')
#         time.sleep(5)  # Simulate task work

# @receiver(task_received)
# def on_task_received(sender, request, **kwargs):
#     # request.session['jooble'] = False
#     obj = CeleryModel.objects.filter(name='jooble').first()
#     print(f"Session state of Jooble in receicer function before set : "
#           f"{obj.status}")
#     obj.status = False
#     obj.save()
#     print(f"Session state of Jooble in receicer function after set : "
#           f"{obj.status}")
#
#     obj = CeleryModel.objects.filter(name='himalayas').first()
#     print(f"Session state of Jooble in receicer function before set : "
#           f"{obj.status}")
#     obj.status = False
#     obj.save()
#     print(f"Session state of Jooble in receicer function after set : "
#           f"{obj.status}")

# @app.task
# def check_group_scraper(self):
#     print("Group scrapper called")