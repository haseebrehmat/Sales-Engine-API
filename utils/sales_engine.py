import json
import re

import requests
from job_portal.models import SalesEngineJobsStats, JobDetail
from job_portal.utils.keywords_dic import keyword, regular_expressions
from scraper.utils.thread import start_new_thread
from utils.helpers import saveLogs
from settings.base import SALES_ENGINE_UPLOAD_JOBS_URL, SALES_ENGINE_API_TOKEN
from utils.requests_logger import requests_logger_hooks


@start_new_thread
def upload_jobs_in_sales_engine(jobs_data, filename=None):
    try:
        url = SALES_ENGINE_UPLOAD_JOBS_URL

        payload = json.dumps({
            "jobs": [
                {
                    "job_title": job.job_title,
                    "job_source_url": job.job_source_url,
                    "job_type": job.job_type,
                    "job_posted_date": job.job_posted_date.strftime('%Y-%m-%d'),
                    "job_source": job.job_source,
                    "job_description": job.job_description,
                    "company_name": job.company_name,
                    "address": job.address
                } for job in jobs_data]
        }
        )

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

        upload_jobs_in_sales_engine_staging(jobs_data, filename=None)
    except Exception as e:
        saveLogs(e)


def upload_jobs_in_sales_engine_staging(jobs_data, filename=None):
    try:
        headers = {
            'Authorization': '445f188bsk3423dsd1342jj434hjkn43j43n43j4d875ee0995ac1e89de6fc1d0252aabc5f2b24a4928',
            'Content-Type': 'application/json'
        }

        url = 'https://decagon-staging.devsinc.com/job_portal/api/v1/job_roles'  # API for getting role
        resp = requests.get(url, headers=headers)
        job_roles = json.loads(resp.text).get('job_roles', []) if resp.ok else []

        excluded_jobs = ['others', 'others dev', 'other', 'other dev']
        url = 'https://decagon-staging.devsinc.com/job_portal/api/v1/jobs'

        payload = json.dumps({
            "jobs": [
                {
                    'salary_min': job.salary_min,
                    'salary_max': job.salary_max,
                    'tech_stacks': job.tech_keywords,
                    'job_role': check_job_role(job.tech_keywords, job_roles) if job_roles else "N/A",
                    'salary_format': '',
                    "job_title": job.job_title,
                    "job_source_url": job.job_source_url,
                    "job_type": job.job_type,
                    "job_posted_date": job.job_posted_date.strftime('%Y-%m-%d'),
                    "job_source": job.job_source,
                    "job_description": job.job_description,
                    "company_name": job.company_name,
                    "address": job.address
                } for job in jobs_data if job.tech_keywords not in excluded_jobs]
        }
        )

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


def check_job_role(tech, job_roles):
    regular_expression = [item for item in regular_expressions if item['tech_stack'] == tech]

    for role in job_roles:
        for regex in regular_expression:
            pattern = re.compile(regex['exp'])
            if pattern.search(role):
                return role
    else:
        'N/A'
