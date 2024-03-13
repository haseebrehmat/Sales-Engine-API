from rest_framework.views import APIView
from rest_framework.permissions import AllowAny 
import pandas as pd
from rest_framework.response import Response
from scraper.models import JobSourceQuery
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming


class FlaskScrapper(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        scrapper = request.GET.get('scrapper')
        queries = JobSourceQuery.objects.filter(
        job_source=scrapper).values_list('queries', flat=True)
        job_sources = [{'link': query['link'], 'job_type': query['job_type']} for queries_list in queries for query in queries_list]
        data = {
            "scrapper": scrapper,
            "job_source": job_sources
        }
        return Response(data)


class FlaskResponse(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        import pdb
        pdb.set_trace()
        data = request.data

        jobs = data.get('jobs')
        df = pd.DataFrame(jobs)
        print(df)
        filename: str = generate_scraper_filename(ScraperNaming.WE_WORK_REMOTELY)
        df.to_excel(filename, index=False)
        return "data save successfuly"

