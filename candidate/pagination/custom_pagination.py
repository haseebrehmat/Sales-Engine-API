from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from candidate.models import Regions


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'limit'
    max_page_size = 250

    def get_paginated_response(self, data):
        response = Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'num_pages': self.page.paginator.num_pages,
            "regions": self.regions(),
            'results': data,


        })
        return response


    def regions(self):
        return [{"id": x.id, "name": x.region} for x in Regions.objects.all()]