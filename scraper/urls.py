from django.urls import path

from scraper.schedulers.job_upload_scheduler import upload_jobs
from scraper.views.job_source_queries import JobQueriesDetailView, JobQueriesView
from scraper.views.scheduler_settings import SchedulerView, SchedulerDetailView
from scraper.views.sync_scheduler import SyncScheduler, SchedulerStatusView, SyncAllScrapersView
from scraper.views.scraper_logs import ScraperLogView
from scraper.views.group_scraper import GroupScraperView, GroupScraperDetailView, RunGroupScraper
from scraper.views.group_scraper_queries import GroupScraperQueriesView, GroupScraperQueriesDetailView
from scraper.views.account import AccountView, AccountDetailView

urlpatterns = [
    path('sync/', SyncScheduler.as_view(), name="jobs"),
    path('scheduler/', SchedulerView.as_view()),
    path('scheduler/<str:pk>/', SchedulerDetailView.as_view()),
    path('job_source_link/', JobQueriesView.as_view()),
    path('job_source_link/<str:pk>/', JobQueriesDetailView.as_view()),
    path('scheduler_status/', SchedulerStatusView.as_view()),
    path('sync_scheduler/', SyncAllScrapersView.as_view()),
    path('logs/', ScraperLogView.as_view()),
    path('accounts/', AccountView.as_view()),
    path('accounts/<str:pk>/', AccountDetailView.as_view()),
    path('group_scheduler/', GroupScraperView.as_view()),
    path('group_scheduler/<int:pk>/', GroupScraperDetailView.as_view()),
    path('group_scheduler_link/', GroupScraperQueriesView.as_view()),
    path('group_scheduler_link/<int:pk>/', GroupScraperQueriesDetailView.as_view()),
    path('group_scheduler_start/', RunGroupScraper.as_view()),
]
