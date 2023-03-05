"""job_portal URL Configuration"""

from django.urls import path, include
from rest_framework import routers

from dashboard.views import DashboardAnalyticsView
from job_portal.views import JobDetailsView, JobDataUploadView, ChangeJobStatusView, AppliedJobDetailsView, \
    ListAppliedJobView

app_name = 'dashboard_analytics'
urlpatterns = \
    [
        path('dashboard_analytics/', DashboardAnalyticsView.as_view(),name='dashboard_analytics'),
    ]
