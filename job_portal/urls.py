"""job_portal URL Configuration"""

from django.urls import path, include
from rest_framework import routers

from job_portal.views import JobDetailsView, JobDataUploadView, ChangeJobStatusView, AppliedJobDetailsView

router = routers.DefaultRouter()
router.register(r'', JobDetailsView, basename='job_details')

app_name = 'job_portal'
urlpatterns = [
    path('upload_data/', JobDataUploadView.as_view(),name='upload_job_data'),
    path('job_details/', include(router.urls)),
    path('job_status/', ChangeJobStatusView.as_view(), name='change_job_status'),
    path('applied_job_details/', AppliedJobDetailsView.as_view(), name='applied_job_details'),
]
