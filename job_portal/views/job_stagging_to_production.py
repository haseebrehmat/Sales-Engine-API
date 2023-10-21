from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from settings.base import STAGGING_TO_PRODUCTION_API_TOKEN
from authentication.exceptions import InvalidUserException
from job_portal.models import JobDetail
from job_portal.serializers.stagging_to_production import JobDetailSerializer
from rest_framework.response import Response
from datetime import datetime

from utils.sales_engine import upload_jobs_in_sales_engine


class JobsStaggingToProduction(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = JobDetailSerializer

    def post(self, request):
        auth_token = request.META.get("HTTP_AUTHORIZATION")
        # Check or use the auth_token as needed
        if auth_token == STAGGING_TO_PRODUCTION_API_TOKEN:
            try:
                jobs = request.data.get("jobs")
                model_instances = [
                    JobDetail(
                        job_title=job_item.get("job_title", ""),
                        company_name=job_item.get("company_name", ""),
                        job_source=job_item.get("job_source", ""),
                        job_type=job_item.get("job_type", ""),
                        address=job_item.get("address", ""),
                        job_description=job_item.get("job_description", ""),
                        tech_keywords=job_item.get("tech_stacks", "").split(","),
                        job_posted_date=job_item.get("job_posted_date", datetime.now()),
                        job_source_url=job_item.get("job_source_url", ""),
                        salary_format=job_item.get("salary_format", ""),
                        salary_min=job_item.get("salary_min", ""),
                        salary_max=job_item.get("salary_max", ""),
                        job_role=job_item.get("job_role", "")
                    )
                    for job_item in jobs
                ]
                JobDetail.objects.bulk_create(
                    model_instances, ignore_conflicts=True, batch_size=1000)
                upload_jobs_in_sales_engine(model_instances, None)
                message = "Jobs posted successfully"
                status_code = status.HTTP_201_CREATED
                return Response({"detail": message}, status_code)
            except Exception as e:
                message = str(e)
                status_code = status.HTTP_406_NOT_ACCEPTABLE
                return Response({"detail": message}, status_code)
        else:
            message = "You do not have permission to this end point"
            status_code = status.HTTP_406_NOT_ACCEPTABLE
            return Response({"detail": message}, status_code)
