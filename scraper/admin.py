from django.contrib import admin



from scraper.models import SchedulerSettings
from scraper.models import Accounts, SchedulerSync

admin.site.register([SchedulerSettings, Accounts, SchedulerSync])
