import datetime
from django.db.models import Count, Sum
from django.db.models import Q
from rest_framework.generics import ListAPIView
from job_portal.utils.helpers import SalesEngineLogsNaming
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

        queryset = SalesEngineJobsStats.objects.filter(search_query, from_date_query, to_date_query, job_sources_query).order_by('-created_at')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = super(SalesEngineJobsStatsView, self).list(request, *args, **kwargs)
        serialized_data = response.data
        additional_stats = {
            "stagging_to_production": {
                "total_hits": queryset.filter(
                    source=SalesEngineLogsNaming.STAGING_TO_PRODUCTION).count() or 0,
                "total_success_hits": queryset.filter(
                    source=SalesEngineLogsNaming.STAGING_TO_PRODUCTION, upload_status=True).count() or 0,
                "total_failed_hits": queryset.filter(
                    source=SalesEngineLogsNaming.STAGING_TO_PRODUCTION, upload_status=False).count() or 0,
                "total_jobs_count": queryset.filter(
                    source=SalesEngineLogsNaming.STAGING_TO_PRODUCTION).aggregate(
                    jobs=Sum('jobs_count'))['jobs'] or 0,
                "total_success_jobs_count": queryset.filter(
                    source=SalesEngineLogsNaming.STAGING_TO_PRODUCTION, upload_status=True).aggregate(
                    jobs=Sum('jobs_count'))['jobs'] or 0,
                "total_failed_jobs_count": queryset.filter(
                    source=SalesEngineLogsNaming.STAGING_TO_PRODUCTION, upload_status=False).aggregate(
                    jobs=Sum('jobs_count'))['jobs'] or 0
            }
            ,
            "production_to_sales_engine": {
                "total_hits": queryset.filter(
                    source=SalesEngineLogsNaming.PRODUCTION_TO_SALES_ENGINE).count() or 0,
                "total_success_hits": queryset.filter(
                    source=SalesEngineLogsNaming.PRODUCTION_TO_SALES_ENGINE, upload_status=True).count() or 0,
                "total_failed_hits": queryset.filter(
                    source=SalesEngineLogsNaming.PRODUCTION_TO_SALES_ENGINE, upload_status=False).count() or 0,
                "total_jobs_count_from": queryset.filter(
                    source=SalesEngineLogsNaming.PRODUCTION_TO_SALES_ENGINE).aggregate(
                    jobs=Sum('jobs_count'))['jobs'] or 0,
                "total_success_jobs_count": queryset.filter(
                    source=SalesEngineLogsNaming.PRODUCTION_TO_SALES_ENGINE, upload_status=True).aggregate(
                    jobs=Sum('jobs_count'))['jobs'] or 0,
                "total_failed_jobs_count": queryset.filter(
                    source=SalesEngineLogsNaming.PRODUCTION_TO_SALES_ENGINE, upload_status=False).aggregate(
                    jobs=Sum('jobs_count'))['jobs'] or 0
            }
        }
        serialized_data['additional_stats'] = additional_stats
        response.data = serialized_data
        return response