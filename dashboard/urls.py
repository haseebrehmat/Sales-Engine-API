"""job_portal URL Configuration"""

from django.urls import path
from dashboard.views import DashboardAnalyticsView

app_name = 'dashboard_analytics'
urlpatterns = [
        path('dashboard_analytics/', DashboardAnalyticsView.as_view(), name='dashboard_analytics'),
    ]
