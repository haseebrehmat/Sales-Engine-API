"""job_portal URL Configuration"""

from django.urls import path, include
from rest_framework import routers

from job_portal.classifier.update_job_stacks import UpdateJobStackView
from job_portal.views import JobDetailsView, JobDataUploadView, JobCleanerView, ChangeJobStatusView, AppliedJobDetailsView, \
    ListAppliedJobView, MarkedAsExpiredView
from job_portal.views.applied_jobs import AppliedJobView
from job_portal.views.blacklist_jobs_source import BlackListJobsView, JobSourcesView, NonBlackListJobsView
from job_portal.views.cover_letter.download import DownloadCoverView
from job_portal.views.cover_letter.generate_cover import GenerateCoverView
from job_portal.views.generate_analytics import GenerateAnalytics, GenerateAnalytics2
from job_portal.views.get_tech_keywords import get_tech_keywords
from job_portal.views.job_detail import RemoveDuplicateView, JobModification
from job_portal.views.job_company import JobCompaniesList
from job_portal.views.job_upload import JobSourceCleanerView, JobTypeCleanerView
from job_portal.views.manual_job_upload import ManualJobUploadView, ManualJobUploadDetail
from job_portal.views.sales_engine_logs import SalesEngineJobsStatsView
from job_portal.views.trends_analytics import TrendsAnalyticsListView, TrendsAnalyticsDetailView

router1 = routers.DefaultRouter()
router2 = routers.DefaultRouter()
router1.register(r'', JobDetailsView, basename='job_details')
router2.register(r'', MarkedAsExpiredView, basename='expired_jobs')

app_name = 'job_portal'
urlpatterns = [
    path('upload_data/', JobDataUploadView.as_view(), name='upload_job_data'),
    path('manual_jobs/', ManualJobUploadView.as_view()),
    path('job_details/', include(router1.urls)),
    path('expired_jobs/', include(router2.urls)),
    path('job_status/', ChangeJobStatusView.as_view(), name='change_job_status'),
    path('applied_job_details/', AppliedJobDetailsView.as_view(),
         name='applied_job_details'),
    path('team_applied_job_details/', ListAppliedJobView.as_view()),
    path('applied_jobs/', AppliedJobView.as_view(),
         name='team_applied_job_details'),
    path('cover_letter/download/', DownloadCoverView.as_view()),
    path('cover_letter/generate/', GenerateCoverView.as_view()),
    path('clean_job_keywords/', JobCleanerView.as_view()),
    path('company/blacklist/add/', BlackListJobsView.as_view()),
    path('company/blacklist/remove/', NonBlackListJobsView.as_view()),
    path('job_sources/', JobSourcesView.as_view()),
    path('clean_job_type/', JobTypeCleanerView.as_view()),
    path('clean_job_source/', JobSourceCleanerView.as_view()),
    path('clean_job_techstacks/', UpdateJobStackView.as_view()),
    path('tech_keywords/', get_tech_keywords),
    path('delete_duplicated_jobs/', RemoveDuplicateView.as_view()),
    path('all_job_companies/', JobCompaniesList.as_view()),
    path('sales_engine_logs/', SalesEngineJobsStatsView.as_view()),
    path('generate_analytics/', GenerateAnalytics2.as_view()),
    # path('generate_analytics2/', GenerateAnalytics2.as_view()),
    path('job_modification/<str:pk>/', JobModification.as_view()),
    path('job_expired_at/<str:pk>/', ManualJobUploadDetail.as_view()),
    path('trends_analytics/', TrendsAnalyticsListView.as_view()),
    path('trends_analytics/<int:pk>/', TrendsAnalyticsDetailView.as_view()),

]

# scheduler.start()
