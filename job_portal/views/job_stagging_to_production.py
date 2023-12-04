from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from settings.base import STAGGING_TO_PRODUCTION_API_TOKEN
from authentication.exceptions import InvalidUserException
from job_portal.models import JobDetail, SalesEngineJobsStats
from job_portal.serializers.stagging_to_production import JobDetailSerializer
from rest_framework.response import Response
from datetime import datetime
from job_portal.utils.helpers import SalesEngineLogsNaming
from utils.sales_engine import upload_jobs_in_sales_engine
from scraper.models.scraper_logs import ScraperLogs


class JobsStaggingToProduction(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = JobDetailSerializer

    def post(self, request):
        auth_token = request.META.get("HTTP_AUTHORIZATION")
        # Check or use the auth_token as needed
        if auth_token == STAGGING_TO_PRODUCTION_API_TOKEN:
            try:
                jobs = request.data.get("jobs")
                logs = request.data.get("logs")
                before_uploaded_jobs = JobDetail.objects.count()
                model_instances = [
                    JobDetail(
                        job_title=job_item.get("job_title", ""),
                        company_name=job_item.get("company_name", ""),
                        job_source=job_item.get("job_source", ""),
                        job_type=job_item.get("job_type", ""),
                        address=job_item.get("address", ""),
                        job_description=job_item.get("job_description", ""),
                        job_description_tags=job_item.get("job_description_tags", ""),
                        tech_stacks=job_item.get("tech_stacks", ""),
                        tech_keywords=job_item.get("tech_keywords", ""),
                        job_posted_date=job_item.get("job_posted_date"),
                        job_source_url=job_item.get("job_source_url", ""),
                        salary_format=job_item.get("salary_format", ""),
                        salary_min=job_item.get("salary_min", ""),
                        salary_max=job_item.get("salary_max", ""),
                        job_role=job_item.get("job_role", "")
                    )
                    for job_item in jobs
                ]

                JobDetail.objects.bulk_create(model_instances, ignore_conflicts=True)
                after_uploading_jobs = JobDetail.objects.count()
                total_uploaded_jobs = after_uploading_jobs - before_uploaded_jobs

                ScraperLogs.objects.create(job_source=logs['job_source'], total_jobs=logs['total_jobs'], filename=logs['filename'], uploaded_jobs=total_uploaded_jobs)
                upload_jobs_in_sales_engine(model_instances, None)
                message = "Jobs posted successfully"
                status_code = status.HTTP_201_CREATED
                try:
                    job_source = model_instances[0].job_source
                    obj = SalesEngineJobsStats.objects.create(job_source=model_instances[0].job_source,
                                                                jobs_count=len(model_instances),
                                                                source=SalesEngineLogsNaming.STAGING_TO_PRODUCTION)
                except:
                    print("")
                return Response({"detail": message}, status_code)
            except Exception as e:
                message = str(e)
                status_code = status.HTTP_406_NOT_ACCEPTABLE
                try:
                    job_source = model_instances[0].job_source
                    obj = SalesEngineJobsStats.objects.create(job_source=model_instances[0].job_source,
                                                                jobs_count=len(model_instances),
                                                                source=SalesEngineLogsNaming.STAGING_TO_PRODUCTION,
                                                                upload_status=False, response=str(e))
                except:
                    print("")
                return Response({"detail": message}, status_code)
        else:
            message = "You do not have permission to this end point"
            status_code = status.HTTP_406_NOT_ACCEPTABLE
            return Response({"detail": message}, status_code)
