import json
import requests
from job_portal.models import SalesEngineJobsStats
from scraper.utils.thread import start_new_thread
from utils.helpers import saveLogs
from settings.base import SALES_ENGINE_UPLOAD_JOBS_URL, SALES_ENGINE_API_TOKEN
from utils.requests_logger import requests_logger_hooks


@start_new_thread
def upload_jobs_in_sales_engine(jobs_data, filename=None):
    try:
        url = SALES_ENGINE_UPLOAD_JOBS_URL

        payload = json.dumps({"jobs": [
            {"job_title": job.job_title, "job_source_url": job.job_source_url, "job_type": job.job_type,
             "job_posted_date": job.job_posted_date.strftime('%Y-%m-%d'), "job_source": job.job_source,
             "job_description": job.job_description, "company_name": job.company_name, "address": job.address} for
            job
            in jobs_data]})

        headers = {
            'Authorization': SALES_ENGINE_API_TOKEN,
            'Content-Type': 'application/json'}

        response = requests.request("POST", url, headers=headers, data=payload, hooks=requests_logger_hooks)

        # print(response.text)
        if response.ok:
            if filename:
                job_source = filename.replace('scraper/job_data/', '').split(' ')[0]
            else:
                if jobs_data:
                    job_source = jobs_data[0].job_source
            obj = SalesEngineJobsStats.objects.create(job_source=job_source, jobs_count=len(jobs_data))
    except Exception as e:
        saveLogs(e)
