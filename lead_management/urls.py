from django.urls import path
from lead_management.views.status import StatusList, StatusDetail, AllStatuses
from lead_management.views.company_status import CompanyStatusList, CompanyStatusDetail, AllCompanyStatuses, CompanyStatusPhases
from lead_management.views.phase import PhaseList, PhaseDetail

urlpatterns = [
    path('statuses/', StatusList.as_view()),
    path('status_list/', AllStatuses.as_view()),

    path('statuses/<int:pk>/', StatusDetail.as_view()),
    path('company_statuses/', CompanyStatusList.as_view()),
    path('company_statuses/<int:pk>/', CompanyStatusDetail.as_view()),
    path('company_status_phases/', CompanyStatusPhases.as_view()),
    path('phases/', PhaseList.as_view()),
    path('company_status_list/', AllCompanyStatuses.as_view()),
    path('phases/<int:pk>/', PhaseDetail.as_view()),
]
