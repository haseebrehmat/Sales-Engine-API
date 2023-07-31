from django.urls import path

from lead_management.views.company_status import CompanyStatusList, CompanyStatusDetail, AllCompanyStatuses, \
    CompanyStatusPhases
from lead_management.views.lead import LeadDetail
from lead_management.views.lead_activity import LeadActivityList, LeadActivityDetail
from lead_management.views.lead_management import LeadManagement, StatusLeadManagement
from lead_management.views.leads_filters import LeadManagementFilters
from lead_management.views.phase import PhaseList, PhaseDetail
from lead_management.views.status import StatusList, StatusDetail, AllStatuses
from lead_management.views.lead_activity_notes import LeadActivityNotesList, LeadActivityNotesDetail

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
    path('leads/', StatusLeadManagement.as_view()),
    path('leads/<str:pk>/', LeadDetail.as_view()),
    path('lead_activities/', LeadActivityList.as_view()),
    path('lead_activities/<int:pk>/', LeadActivityDetail.as_view()),
    path('lead_activity_notes/', LeadActivityNotesList.as_view()),
    path('lead_activity_notes/<int:pk>/', LeadActivityNotesDetail.as_view()),
    path('leads_data/', LeadManagement.as_view()),
    path('leads_filters/', LeadManagementFilters.as_view()),
]
