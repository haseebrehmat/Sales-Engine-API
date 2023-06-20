from django.db.models import Q
from rest_framework import pagination
from rest_framework.response import Response

from job_portal.models import BlockJobCompany


class JobCompanyPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 500
    page_query_param = 'page'

    def get_paginated_response(self, data, queryset):
        total_job_companies = len(queryset) if queryset else 0
        blocked_job_companies = self.get_blocked_job_companies_count()
        response = Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'num_pages': self.page.paginator.num_pages
            },
            'data': data,
            'job_companies_stats': {
                'total': total_job_companies,
                "blocked": blocked_job_companies,
                "unblocked": total_job_companies - blocked_job_companies,
            }

        })
        return response

    def get_blocked_job_companies_count(self):
        search = self.request.query_params['search']
        search_query = Q()
        if search:
            search = search.lower()
            search_query = Q(company_name__icontains=search)
        block_job_companies = list(
            BlockJobCompany.objects.filter(company=self.request.user.profile.company).filter(search_query).values_list(
                'company_name',
                flat=True))
        return len(block_job_companies)
