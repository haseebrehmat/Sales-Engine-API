from django.contrib import admin



from scraper.models import SchedulerSettings
from scraper.models import Accounts, SchedulerSync
from scraper.models.group_scraper import GroupScraper
from scraper.models.group_scraper_query import GroupScraperQuery
from scraper.models.job_sources import JobSource
from scraper.models.scraper_logs import ScraperLogs

admin.site.register([SchedulerSettings, Accounts, SchedulerSync, GroupScraper, GroupScraperQuery, JobSource, ScraperLogs])
