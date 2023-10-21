import json
import re
from datetime import datetime, timedelta

import requests
from job_portal.models import SalesEngineJobsStats, JobDetail
from job_portal.utils.keywords_dic import keyword, regular_expressions
from scraper.models import RestrictedJobsTags
from scraper.utils.thread import start_new_thread
from utils.helpers import saveLogs
from settings.base import SALES_ENGINE_UPLOAD_JOBS_URL, SALES_ENGINE_API_TOKEN, env, STAGGING_TO_PRODUCTION_API_TOKEN
from utils.requests_logger import requests_logger_hooks

# restricted_job_tags = ['banking', 'government', 'federal', 'crypto', 'ether', 'clearance',
#                        'army, navy, seals, air force', 'government advisory services', 'gambling', 'clearance',
#                        'adult', 'music', 'alcohol', 'wine', 'dating', 'lgbt', 'weapons']

# removing 'insurance' from restricted job tags, Having conflicts with health insurance

excluded_jobs_tech = ['others', 'others dev', 'other']

job_roles_dict = {
    "sqa": ['qa'],
    "dev": ['shopify', 'ruby on rails', 'service now', 'ml engineer',
            'data engineering/data engineer', 'data science/data scientist', 'c#/dot net',
            'c/c++', 'php', 'python', 'go/golang', 'java', 'mern', 'javascript', 'ui/ux',
            'networking', 'database'],
    "devops": ['devops'],
    "mobile": ['ios', 'flutter', 'android', 'react native'],
    "dynamic 365": ['dynamics'],
    "metaverse": ['metaverse'],
    "blockchain": ['blockchain'],
    "salesforce": ['salesforce']
}


def filter_restricted_jobs(jobs):
    restricted_job_tags = RestrictedJobsTags.objects.exclude(tag=None).values_list('tag', flat=True)
    jobs = [job for job in jobs if
            all(i not in job['job_title'] and i not in job['job_description'] for i in restricted_job_tags)]

    return jobs


@start_new_thread
def upload_jobs_in_sales_engine(jobs_data, filename=None):
    try:
        headers = {
            'Authorization': SALES_ENGINE_API_TOKEN,
            'Content-Type': 'application/json'
        }

        url = 'https://bd.devsinc.com/job_portal/api/v1/job_roles'  # API for getting role
        resp = requests.get(url, headers=headers)
        job_roles = json.loads(resp.text).get('job_roles', []) if resp.ok else []

        url = SALES_ENGINE_UPLOAD_JOBS_URL
        jobs = [
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
            } for job in jobs_data if job.tech_keywords not in excluded_jobs_tech]
        before_filter = jobs
        jobs = filter_restricted_jobs(jobs)

        payload = json.dumps(
            {
                "jobs": jobs
            }
        )

        if env("ENVIRONMENT") == 'local':
            for x in json.loads(payload)['jobs']:
                print('Title => ', x['job_title'], 'Job Role => ', x['job_role'])

        if env("ENVIRONMENT") == "production":
            response = requests.request("POST", url, headers=headers, data=payload, hooks=requests_logger_hooks)

            print(response.text)
            if response.ok:
                if filename:
                    job_source = filename.replace('scraper/job_data/', '').split(' ')[0]
                else:
                    if jobs_data:
                        job_source = jobs_data[0].job_source
                obj = SalesEngineJobsStats.objects.create(job_source=job_source, jobs_count=len(jobs))

    except Exception as e:
        saveLogs(e)


def check_job_role(techstacks, job_roles):
    try:
        job_roles.remove('N/A')
    except:
        pass
    techstacks = techstacks.lower().split(',')
    job_roles_data = set()
    try:

        for tech in techstacks:
            regular_expression = [item for item in regular_expressions if item['tech_stack'].lower() == tech.lower()]

            for role in job_roles:
                for regex in regular_expression:
                    pattern = re.compile(regex['exp'])
                    if pattern.search(role):
                        job_roles_data.add(role)
            else:
                for x in job_roles:
                    if tech.lower() in job_roles_dict[x.lower()]:
                        job_roles_data.add(x)
        if job_roles_data:
            job_roles_data = list(job_roles_data)
            return "Dev" if len(job_roles_data) > 1 else job_roles_data[0] if job_roles_data else 'N/A'
    except Exception as e:
        print(e)
        if job_roles_data:
            job_roles_data = list(job_roles_data)
            return "Dev" if len(job_roles_data) > 1 else job_roles_data[0] if job_roles_data else 'N/A'




@start_new_thread
def upload_jobs_in_production(jobs_data, filename=None):
    try:
        headers = {
            'Authorization': STAGGING_TO_PRODUCTION_API_TOKEN,
            'Content-Type': 'application/json'
        }

        host = 'http://18.208.86.195/'
        if env('ENVIRONMENT') == 'local':
            host = 'http://127.0.0.1:8000/'
        url = host + 'api/job_portal/jobs_stagging_to_production/'
        jobs = [
            {
                'salary_min': job.salary_min,
                'salary_max': job.salary_max,
                'tech_stacks': job.tech_keywords,
                'job_role': "N/A",
                'salary_format': '',
                "job_title": job.job_title,
                "job_source_url": job.job_source_url,
                "job_type": job.job_type,
                "job_posted_date": job.job_posted_date.strftime('%Y-%m-%d'),
                "job_source": job.job_source,
                "job_description": job.job_description,
                "company_name": job.company_name,
                "address": job.address
            } for job in jobs_data]


        payload = json.dumps(
            {
                "jobs": jobs
            }
        )

        if env("ENVIRONMENT") != 'production':
            response = requests.request("POST", url, headers=headers, data=payload, hooks=requests_logger_hooks)
            print(response.text)
            if response.ok:
                print("Jobs posted successfully")
            else:
                print("Jobs posted unsuccessfully")
        print("")
    except Exception as e:
        saveLogs(e)