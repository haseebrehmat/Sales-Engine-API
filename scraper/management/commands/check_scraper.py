import time
from django.utils import timezone
from scraper.models.scheduler import SchedulerSync
from scraper.models.group_scraper import GroupScraper
from datetime import datetime
from django.core.management.base import BaseCommand
from scraper.schedulers.job_upload_scheduler import change_group_scraper_id_from_celery

class Command(BaseCommand):
    help = 'Run a specific Python file'
    def handle(self, *args, **options):
        custom_function()

def custom_function():
    group_scrapper = check_current_group()
    check_status = SchedulerSync.objects.filter(
            type="group scraper", job_source=group_scrapper.name.lower()).first()
    change_group_scraper_id_from_celery(group_scrapper.id)

def check_current_group():
    group_scrapper = None
    queryset = GroupScraper.objects.all().order_by('scheduler_settings__time')
    for index, groupscraper in enumerate(queryset):
        # Get the formatted time and the scheduler settings time
        current_time = timezone.now()
        formatted_time = current_time.strftime("%H:%M:%S")  # Replace with your time format
        formatted_time = datetime.strptime(formatted_time, "%H:%M:%S").time()

        # Get the current and next scheduler settings times
        current_time = queryset[index].scheduler_settings.time
        next_time = queryset[index + 1].scheduler_settings.time if index + 1 < len(queryset) else None

        # Check if formatted_time is within the range of current_time and next_time
        if next_time is not None:
            if formatted_time >= current_time and formatted_time < next_time:
                group_scrapper = queryset[index]
                break
        else:
            group_scrapper = queryset[index]
            break
    return group_scrapper


