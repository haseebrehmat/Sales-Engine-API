from rest_framework import pagination
from rest_framework.response import Response

from job_portal.utils.keywords_dic import get_tech_stacks


class TrendAnalyticsPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data):
        response = Response({'links': {'next': self.get_next_link(), 'previous': self.get_previous_link(),
                                       'num_pages': self.page.paginator.num_pages}, 'data': data, 'tech_stacks': get_tech_stacks() })
        return response
