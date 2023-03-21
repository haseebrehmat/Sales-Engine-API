from django.urls import path

from job_scraper.views.sync_scheduler import SyncScheduler

urlpatterns = [
  path('sync/', SyncScheduler.as_view(), name="jobs"),
]

# scheduler.start()
