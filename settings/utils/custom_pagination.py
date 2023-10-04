from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response

from candidate.models import Regions


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'limit'
    max_page_size = 250

    def get_paginated_response(self, data):
        response = Response(
            {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'num_pages': self.page.paginator.num_pages,
                'results': data
            }
        )
        return response


class CustomCursorPagination(CursorPagination):
    page_size = 50
    max_page_size = 250
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        response = Response(
            {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data,
                'max_page_size': self.max_page_size,
                'min_page_size': self.page_size,
                'page_limits': [x for x in range(self.page_size, self.max_page_size + 1, 50)]
            }
        )
        return response
