from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import pandas as pd
from scraper.utils.helpers import generate_scraper_filename
from scraper.schedulers.job_upload_scheduler import upload_jobs


class FlaskResponse(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        jobs = request.data.get('jobs')
        job_source = request.data.get('job_source')
        df = pd.DataFrame(jobs)
        print(df)
        filename: str = generate_scraper_filename(job_source)
        df.to_excel(filename, index=False)
        upload_jobs('instant', job_source)
        return "data save successfuly"
