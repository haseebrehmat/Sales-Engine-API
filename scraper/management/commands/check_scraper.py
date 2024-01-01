import time
import pytz
from django.utils import timezone
from settings.base import ENVIRONMENT, env
from scraper.models.scheduler import SchedulerSync
from scraper.models.group_scraper import GroupScraper
from datetime import datetime
from django.core.management.base import BaseCommand
from scraper.schedulers.job_upload_scheduler import group_scraper_job

class Command(BaseCommand):
    help = 'Run a specific Python file'
    def handle(self, *args, **options):
        custom_function()

def custom_function():
    group_scrapper = check_current_group()
    check_status = SchedulerSync.objects.filter(
            type="group scraper", job_source=group_scrapper.name.lower()).first()
    group_scraper_job(group_scrapper.id)

def check_current_group():
    group_scrapper = None
    if env('ENVIRONMENT') == 'production' or env('ENVIRONMENT') == 'development' or env('ENVIRONMENT') == 'local':
        queryset = GroupScraper.objects.filter(disabled=False, is_analytics=False).order_by('scheduler_settings__time')
    if env('ENVIRONMENT') == 'analytics':
        queryset = GroupScraper.objects.filter(disabled=False, is_analytics=True).order_by('scheduler_settings__time')
    for index, groupscraper in enumerate(queryset):
        pakistan_timezone = pytz.timezone('Asia/Karachi')
        current_time = datetime.now(pakistan_timezone)
        formatted_time = current_time.strftime("%H:%M:%S")
        formatted_time = datetime.strptime(formatted_time, "%H:%M:%S").time()

        current_time = queryset[index].scheduler_settings.time
        next_time = queryset[index + 1].scheduler_settings.time if index + 1 < len(queryset) else None
        if next_time is not None:
            if formatted_time >= current_time and formatted_time < next_time:
                group_scrapper = queryset[index]
                break
        else:
            group_scrapper = queryset[index]
            break
    return group_scrapper

