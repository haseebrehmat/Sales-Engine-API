import json
import requests
from job_portal.models import SalesEngineJobsStats
from scraper.utils.thread import start_new_thread
from utils.helpers import saveLogs

@start_new_thread
def upload_jobs_in_sales_engine(jobs_data):
    try:
        url = "https://sales-test.devsinc.com/job_portal/api/v1/jobs"

        payload = json.dumps({"jobs": [
            {"job_title": job.job_title, "job_source_url": job.job_source_url, "job_type": job.job_type,
             "job_posted_date": job.job_posted_date.strftime('%Y-%m-%d'), "job_source": job.job_source,
             "job_description": job.job_description, "company_name": job.company_name, "address": job.address} for
            job
            in jobs_data]})

        headers = {
            'Authorization': '445f188bsk3423dsd1342jj434hjkn43j43n43j4d875ee0995ac1e89de6fc1d0252aabc5f2b24a4928',
            'Content-Type': 'application/json'}

        response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.text)
        if response.ok:
            obj = SalesEngineJobsStats.objects.create(jobs_count=len(jobs_data))
    except Exception as e:
        saveLogs(e)
