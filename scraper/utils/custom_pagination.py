from django.db.models import Sum
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import datetime
from scraper.models import ScraperLogs


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'limit'
    max_page_size = 250

    def get_paginated_response(self, data):
        job_source_analytics = self.get_job_source_analytics()
        response = Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'num_pages': self.page.paginator.num_pages,
            'job_source_analytics': job_source_analytics['stats'],
            'total_scraped_jobs': job_source_analytics['total_scraped_jobs'],
            'total_uploaded_jobs': job_source_analytics['total_uploaded_jobs'],
            'results': data
        })
        return response

    def get_job_source_analytics(self):
        queryset = ScraperLogs.objects.all()
        params = self.request.query_params
        from_date = params['from_date']
        to_date = params['to_date']


        if from_date:
            from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
            queryset = queryset.filter(created_at__gte=from_date)
        if to_date:
            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
            queryset = queryset.filter(created_at__lt=to_date + datetime.timedelta(days=1))
        job_source_analytics = list(
            queryset.values('job_source').annotate(total_scraper_jobs=Sum('total_jobs'),
                                                                    total_uploaded_jobs=Sum('uploaded_jobs')))
        total_scraped_jobs = sum([value['total_scraper_jobs'] for value in job_source_analytics])
        total_uploaded_jobs = sum([value['total_uploaded_jobs'] for value in job_source_analytics])

        return {'total_scraped_jobs': total_scraped_jobs,
                'total_uploaded_jobs': total_uploaded_jobs,
                'stats': job_source_analytics}
