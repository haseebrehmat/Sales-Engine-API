from django.urls import path

from job_scraper.views.job_source_queries import JobQueriesDetailView, JobQueriesView
from job_scraper.views.scheduler_settings import SchedulerView, SchedulerDetailView
from job_scraper.views.scraper_logs import ScraperLogView
from job_scraper.views.sync_scheduler import SyncScheduler, SchedulerStatusView

urlpatterns = [
    path('sync/', SyncScheduler.as_view(), name="jobs"),
    path('scheduler/', SchedulerView.as_view()),
    path('scheduler/<str:pk>/', SchedulerDetailView.as_view()),
    path('job_source_link/', JobQueriesView.as_view()),
    path('job_source_link/<str:pk>/', JobQueriesDetailView.as_view()),
    path('scheduler_status/', SchedulerStatusView.as_view()),
    path('logs/', ScraperLogView.as_view()),
]

