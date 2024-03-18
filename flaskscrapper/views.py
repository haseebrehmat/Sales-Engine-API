from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import pandas as pd
from scraper.utils.helpers import generate_scraper_filename
from scraper.schedulers.job_upload_scheduler import upload_jobs
from rest_framework import status
from rest_framework.response import Response


class JobsPoster(APIView):
    permission_classes = (AllowAny,)
    responsee = Response(
        {"message": "Data saved successfully"},
        status=status.HTTP_200_OK
    )

    def post(self, request):
        jobs = request.data.get('jobs')
        job_source = request.data.get('job_source')
        validated = self.validate_data(jobs, job_source)
        if validated:
            df = pd.DataFrame(jobs)
            filename: str = generate_scraper_filename(job_source)
            df.to_excel(filename, index=False)
            upload_jobs('instant', job_source)

        return self.responsee

    def validate_data(self, jobs, source):
        if not jobs or not source:
            self.responsee = Response(
                {"message": "Jobs data or job source is missing"},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
            return False

        if not len(jobs) == 0:
            self.responsee = Response(
                {"message": "No jobs data provided"},
                status=status.HTTP_204_NO_CONTENT
            )
            return False

        return True
