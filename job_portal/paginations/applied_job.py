import datetime

from rest_framework import pagination
from rest_framework.response import Response

from job_portal.models import JobDetail
from job_portal.utils.job_status import JOB_STATUS_CHOICE


class AppliedJobPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'page'
    query = JobDetail.objects.all()

    def get_paginated_response(self, data):

        response = Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'num_pages': self.page.paginator.num_pages
            },
            'filtered_jobs': self.page.paginator.count,
            'data': data,
            'job_status_choice': dict(JOB_STATUS_CHOICE),
        })
        return response
