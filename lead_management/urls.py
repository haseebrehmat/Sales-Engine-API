from django.urls import path
from lead_management.views.status import StatusList, StatusDetail
from lead_management.views.company_status import CompanyStatusList, CompanyStatusDetail

urlpatterns = [
    path('statuses/', StatusList.as_view()),
    path('statuses/<int:pk>/', StatusDetail.as_view()),
    path('company_statuses/', CompanyStatusList.as_view()),
    path('company_statuses/<int:pk>/', CompanyStatusDetail.as_view()),
]
