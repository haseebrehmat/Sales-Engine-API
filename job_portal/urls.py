"""job_portal URL Configuration"""

from django.urls import path, include
from rest_framework import routers

from job_portal.views import JobDetailsView, JobDataUploadView, JobCleanerView, ChangeJobStatusView, AppliedJobDetailsView, \
    ListAppliedJobView
from job_portal.views.blacklist_jobs_source import BlackListJobsView, JobSourcesView
from job_portal.views.cover_letter.download import DownloadCoverView
from job_portal.views.cover_letter.generate_cover import GenerateCoverView
from job_portal.views.job_upload import JobSourceCleanerView, JobTypeCleanerView

router = routers.DefaultRouter()
router.register(r'', JobDetailsView, basename='job_details')

app_name = 'job_portal'
urlpatterns = [
    path('upload_data/', JobDataUploadView.as_view(), name='upload_job_data'),
    path('job_details/', include(router.urls)),
    path('job_status/', ChangeJobStatusView.as_view(), name='change_job_status'),
    path('applied_job_details/', AppliedJobDetailsView.as_view(),
         name='applied_job_details'),
    path('team_applied_job_details/', ListAppliedJobView.as_view(),
         name='team_applied_job_details'),
    path('cover_letter/download/', DownloadCoverView.as_view()),
    path('cover_letter/generate/', GenerateCoverView.as_view()),
    path('clean_job_keywords/', JobCleanerView.as_view()),
    path('blacklist/jobs/', BlackListJobsView.as_view()),
    path('job_sources/', JobSourcesView.as_view()),
    path('clean_job_type/', JobTypeCleanerView.as_view()),
    path('clean_job_source/', JobSourceCleanerView.as_view()),
]
