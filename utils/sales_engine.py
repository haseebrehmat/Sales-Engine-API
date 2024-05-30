import json
import re
from django.utils import timezone
import requests

from job_portal.models import SalesEngineJobsStats
from job_portal.utils.keywords_dic import regular_expressions
from scraper.models import RestrictedJobsTags
from scraper.utils.thread import start_new_thread
from settings.base import SALES_ENGINE_UPLOAD_JOBS_URL, SALES_ENGINE_API_TOKEN, env, STAGGING_TO_PRODUCTION_API_TOKEN
from utils.helpers import saveLogs
from utils.octagon_slack_bot import send_server_message
from utils.requests_logger import requests_logger_hooks
from scraper.models.scraper_logs import ScraperLogs

# restricted_job_tags = ['banking', 'government', 'federal', 'crypto', 'ether', 'clearance',
#                        'army, navy, seals, air force', 'government advisory services', 'gambling', 'clearance',
#                        'adult', 'music', 'alcohol', 'wine', 'dating', 'lgbt', 'weapons']

# removing 'insurance' from restricted job tags, Having conflicts with health insurance

excluded_jobs_tech = ['others', 'others dev', 'other']
excluded_vals = ['', ' ', 'n/a', 'N/A']

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

def is_sales_engine_restricted_job(job):
    RESTRICTED_COMPANIES = ["jobbot", "remoteworkerus", "braintrust", "dice"]
    job_source = ['linkedin']
    if job.job_source.lower() not in job_source:
        return True
    elif job.company_name.lower() not in RESTRICTED_COMPANIES:
        return True
    else:
        return False

def is_valid_sales_engine_job(job):
    valid_start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) - timezone.timedelta(days=2)
    keywords_condition = job.tech_keywords and job.tech_keywords not in excluded_jobs_tech
    restriced_company_condition = is_sales_engine_restricted_job(job)
    posted_date_condition = str(job.job_posted_date) >= str(valid_start_date)
    company_name_condition = job.company_name and job.company_name.strip() and job.company_name.strip().lower() != 'n/a'
    job_type_condition = job.job_type and job.job_type.strip() and job.job_type.strip().lower() != 'n/a'
    return keywords_condition and restriced_company_condition and posted_date_condition and company_name_condition and job_type_condition


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
                'tech_stacks': job.tech_keywords.replace('ai/ml engineer', 'ai/ml engineer,ai,ml engineer'),
                'job_role': check_job_role(job.tech_keywords, job_roles) if job_roles else "N/A",
                'salary_format': '',
                "job_title": job.job_title,
                "job_source_url": job.job_source_url,
                "job_type": job.job_type,
                "job_posted_date": str(job.job_posted_date),
                "job_source": job.job_source,
                "job_description": job.job_description,
                "company_name": job.company_name,
                "address": job.address
            } for job in jobs_data if is_valid_sales_engine_job(job) and 'remote' in job.job_type.lower() and 'hybrid' not in job.job_type.lower()]

        before_filter = jobs
        jobs = filter_restricted_jobs(jobs)
        if len(jobs) == 0:
            saveLogs("Jobs array is Empty.", 'INFO')
            print("Total Uploaded Jobs: 0")
            return
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
            else:
                if jobs_data:
                    job_source = jobs_data[0].job_source
                    SalesEngineJobsStats.objects.create(job_source=job_source, jobs_count=len(jobs),
                                                        upload_status=False, response=response.text, payload=payload)


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
                    if x.lower() in job_roles_dict and tech.lower() in job_roles_dict[x.lower()]:
                        job_roles_data.add(x)
        if job_roles_data:
            job_roles_data = list(job_roles_data)
            return "Dev" if len(job_roles_data) > 1 else job_roles_data[0] if job_roles_data else 'N/A'
        else:
            return 'N/A'
    except Exception as e:
        print("Error during role assignment => ", e)
        if job_roles_data:
            job_roles_data = list(job_roles_data)
            return "Dev" if len(job_roles_data) > 1 else job_roles_data[0] if job_roles_data else 'N/A'
        else:
            return 'N/A'




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
                'tech_stacks': job.tech_stacks,
                'tech_keywords': job.tech_keywords,
                'job_role': "N/A",
                'salary_format': job.salary_format,
                "job_title": job.job_title,
                "job_source_url": job.job_source_url,
                "estimated_salary": job.estimated_salary,
                "job_type": job.job_type,
                "job_posted_date": str(job.job_posted_date),
                "job_source": job.job_source,
                "job_description": job.job_description,
                "job_description_tags": job.job_description_tags,
                "company_name": job.company_name,
                "address": job.address
            } for job in jobs_data]

        logs = ScraperLogs.objects.filter(filename=filename).first()

        scraper_log = {
            'job_source': str(logs.job_source),
            'total_jobs': str(logs.total_jobs),
            'filename': str(logs.filename),
            'uploaded_jobs': str(logs.uploaded_jobs),
        }

        payload = json.dumps(
            {
                "jobs": jobs,
                "logs": scraper_log
            }
        )

        if env("ENVIRONMENT") != 'production':
            try:
                response = requests.request("POST", url, headers=headers, data=payload, hooks=requests_logger_hooks)
                if response.ok:
                    print("Jobs posted successfully")
                else:
                    print("Jobs posted unsuccessfully")
            except:
                send_server_message(msg=":rotating_light: :rotating_light:  Octagon production server is down. Please fix it ASAP. :rotating_light: :rotating_light:")
    except Exception as e:
        saveLogs(e)
