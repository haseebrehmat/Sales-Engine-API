import datetime

from django.db.models import Q
from rest_framework.generics import ListAPIView

from job_portal.models import SalesEngineJobsStats
from job_portal.paginations.sales_engine import SalesEngineJobsStatsPagination
from job_portal.serializers.Sales_engine_jobs_stats import SalesEngineJobsStatsSerializer


class SalesEngineJobsStatsView(ListAPIView):
    serializer_class = SalesEngineJobsStatsSerializer
    pagination_class = SalesEngineJobsStatsPagination

    def get_queryset(self):
        params = self.request.query_params

        search_query = Q()
        from_date_query = Q()
        to_date_query = Q()
        job_sources_query = Q()

        search = params.get('search')
        from_date = params.get('from_date')
        to_date = params.get('to_date')
        job_sources = params.get('job_sources')

        if search:
            search_query = Q(job_source__icontains=search)

        if from_date:
            from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
            from_date_query = Q(created_at__gte=from_date)

        if to_date:
            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
            to_date_query = Q(created_at__lt=to_date + datetime.timedelta(days=1))

        if job_sources:
            job_sources_query = Q(job_source__in=job_sources.split(','))

        queryset = SalesEngineJobsStats.objects.filter(search_query, from_date_query, to_date_query, job_sources_query)
        return queryset
