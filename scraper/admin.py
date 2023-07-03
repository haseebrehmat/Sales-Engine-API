from django.contrib import admin



from scraper.models import SchedulerSettings
from scraper.models import Accounts

admin.site.register([SchedulerSettings, Accounts])
