import datetime
import json
import os
import traceback

import pandas as pd
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.db import transaction
from django.db.models import Q
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from job_portal.classifier import JobClassifier
from job_portal.data_parser.job_parser import JobParser
from job_portal.models import JobDetail, JobUploadLogs, JobArchive, SalesEngineJobsStats
from scraper.jobs import single_scrapers_functions
from scraper.jobs.adzuna_scraping import adzuna_scraping
from scraper.jobs.careerbuilder_scraping import career_builder
from scraper.jobs.careerjet_scraping import careerjet
from scraper.jobs.dice_scraping import dice
from scraper.jobs.glassdoor_scraping import glassdoor
from scraper.jobs.google_careers_scraping import google_careers
from scraper.jobs.indeed_scraping import indeed
from scraper.jobs.jooble_scraping import jooble
from scraper.jobs.linkedin_scraping import linkedin
from scraper.jobs.monster_scraping import monster
from scraper.jobs.simply_hired_scraping import simply_hired
from scraper.jobs.talent_scraping import talent
from scraper.jobs.ziprecruiter_scraping import ziprecruiter_scraping
from scraper.models import JobSourceQuery, GroupScraper, ScraperLogs
from scraper.models import SchedulerSettings, AllSyncConfig
from scraper.models.scheduler import SchedulerSync
from scraper.utils.helpers import convert_time_into_minutes
from scraper.utils.thread import start_new_thread
from settings.base import env
from utils import upload_to_s3
from utils.helpers import saveLogs
from utils.sales_engine import upload_jobs_in_sales_engine

# from error_logger.models import Log
# from scraper.utils.thread import start_new_thread
# from celery import shared_task
# logger = logging.getLogger(__name__)

scraper_functions = {
    "linkedin": [
        linkedin,  # Tested working
    ],
    "indeed": [
        indeed,  # Tested working
    ],
    "dice": [
        dice,  # Tested working
    ],
    "careerbuilder": [
        career_builder,  # Test working
    ],
    "glassdoor": [
        glassdoor,  # Tested working
    ],
    "monster": [
        monster,  # Tested working
    ],
    "simplyhired": [
        simply_hired,  # Tested working
    ],
    "ziprecruiter": [
        ziprecruiter_scraping,  # not working
    ],
    "adzuna": [
        adzuna_scraping,
    ],
    "googlecareers": [
        google_careers,
    ],
    "jooble": [
        jooble,
    ],
    "talent": [
        talent,
    ],
    "careerjet": [
        careerjet,
    ]
}


def upload_jobs():
    try:
        print('Uploading files ...')
        path = 'scraper/job_data/'
        temp = os.listdir(path)
        files = [path + file for file in temp]
        for file in files:
            try:
                if not is_file_empty(file):
                    job_parser = JobParser([file])
                    # validate files first
                    is_valid, message = job_parser.validate_file()
                    if is_valid:
                        job_parser.parse_file()
                    upload_to_s3.upload_job_files(file, file.replace(path, ""))
                    upload_file(job_parser, file)
            except Exception as e:
                print(f"An exception occurred: {e}\n\nTraceback: {traceback.format_exc()}")
                saveLogs(e)
    except Exception as e:
        print(f"An exception occurred: {e}\n\nTraceback: {traceback.format_exc()}")
        saveLogs(e)


def is_file_empty(file):
    try:
        valid_extensions = ['.csv', '.xlsx', '.ods', 'odf', '.odt']
        ext = ""
        if isinstance(file, str):
            for x in valid_extensions:
                if x in file:
                    ext = x
                    break

        else:
            ext = os.path.splitext(file.name)[1]
        if ext == ".csv":
            df = pd.read_csv(file, engine='c', nrows=1)
        else:
            df = pd.read_excel(file, nrows=1)
        return df.empty
    except Exception as e:
        saveLogs(e)
        return True


def remove_files(job_source="all"):
    try:
        print("removing files ...")
        if "simply" in job_source:
            job_source = "simply"
        if "career" in job_source:
            job_source = "career"
        if "google" in job_source:
            job_source = "google"
        folder_path = 'scraper/job_data'
        files = os.listdir(folder_path)

        # Loop through the files and remove each one
        for file_name in files:
            if job_source in file_name or job_source == "all":
                file_path = os.path.join(folder_path, file_name)
                try:
                    os.remove(file_path)
                    print(f"Removed {file_path}")
                except Exception as e:
                    msg = f"Failed to remove {file_path}. Error: {str(e)}"
                    print(msg)
                    saveLogs(e)
        print("Files removed successfully ...")
    except Exception as e:
        saveLogs(e)
        print(e)


@transaction.atomic
def upload_file(job_parser, filename):
    # parse, classify and upload data to database
    classify_data = JobClassifier(job_parser.data_frame)
    classify_data.classify()
    before_uploading_jobs = JobDetail.objects.count()

    # last_10_days = datetime.datetime.now() - datetime.timedelta(days=10)
    #
    # query = Q()
    # for item in classify_data.data_frame.itertuples():
    #     query |= Q(company_name=item.company_name, job_title=item.job_title)

    # jobs = JobDetail.objects.filter(query, created_at__lte=last_10_days, job_applied="not applied")

    # bulk_data = [JobArchive(
    #     id=x.id,
    #     job_title=x.job_title,
    #     company_name=x.company_name,
    #     job_source=x.job_source,
    #     job_type=x.job_type,
    #     address=x.address,
    #     job_description=x.job_description,
    #     tech_keywords=x.tech_keywords,
    #     job_posted_date=x.job_posted_date,
    #     job_source_url=x.job_source_url,
    #     block=x.block,
    #     is_manual=x.is_manual,
    #     created_at=x.created_at,
    #     updated_at=x.updated_at
    # ) for x in jobs]
    #
    # JobArchive.objects.bulk_create(bulk_data, ignore_conflicts=True)
    # jobs.delete()

    model_instances = [
        JobDetail(job_title=job_item.job_title,
                  company_name=job_item.company_name,
                  job_source=job_item.job_source,
                  job_type=job_item.job_type,
                  address=job_item.address,
                  job_description=job_item.job_description,
                  tech_keywords=job_item.tech_keywords.replace(" / ", "").lower(),
                  job_posted_date=job_item.job_posted_date,
                  job_source_url=job_item.job_source_url, )
        for job_item in classify_data.data_frame.itertuples() if
        job_item.job_source_url != "" and isinstance(job_item.job_source_url,
                                                     str)]

    JobDetail.objects.bulk_create(
        model_instances, ignore_conflicts=True, batch_size=1000)
    upload_jobs_in_sales_engine(model_instances, filename)
    after_uploading_jobs_count = JobDetail.objects.count()
    scraper_log = ScraperLogs.objects.filter(filename=filename, uploaded_jobs=0).first()
    if scraper_log:
        uploaded_count = after_uploading_jobs_count - before_uploading_jobs
        if uploaded_count > 0:
            scraper_log.uploaded_jobs = uploaded_count
            scraper_log.save()


def get_job_source_quries(job_source):
    job_source_queries = list(JobSourceQuery.objects.filter(
        job_source=job_source).values_list("queries", flat=True))
    return job_source_queries[0] if len(job_source_queries) > 0 else job_source_queries


def get_scrapers_list(job_source):
    scrapers = {}
    if job_source != "all":
        if job_source in list(scraper_functions.keys()):
            try:
                query = get_job_source_quries(job_source)
                function = scraper_functions[job_source]
                if len(function) != 0:
                    scrapers[job_source] = {'stop_status': False, 'function': function[0],
                                            'job_source_queries': query}
            except Exception as e:
                print("error in get scraper function", str(e))
                saveLogs(e)

    else:
        for key in list(scraper_functions.keys()):
            try:
                query = get_job_source_quries(key)
                function = scraper_functions[key]
                if len(function) != 0:
                    function = scraper_functions[key]
                    scrapers[key] = {'stop_status': False, 'function': function[0],
                                     'job_source_queries': query}
            except Exception as e:
                print("error in get scraper function", str(e))
                saveLogs(e)
    return scrapers


def run_scrapers(scrapers):
    # scrapers_without_links = []
    try:
        is_completed = False
        i = 0
        while not is_completed:
            flag = False
            for key in list(scrapers.keys()):
                scraper = scrapers[key]
                scraper_function = scraper['function']
                if not scraper['stop_status']:
                    try:
                        job_source_queries = scraper['job_source_queries']
                        if i < len(job_source_queries):
                            link = job_source_queries[i]['link']
                            job_type = job_source_queries[i]['job_type']
                            scraper_function(link, job_type)
                            flag = True
                        elif not scraper['stop_status']:
                            if i == 0:
                                try:
                                    raise Exception(f'No link for {key}')
                                except Exception as e:
                                    saveLogs(e)
                            scraper['stop_status'] = True
                    except Exception as e:
                        print(e)
                        saveLogs(e)

                    try:
                        upload_jobs()
                        remove_files(key)
                    except Exception as e:
                        print("Error in uploading jobs", e)
                        saveLogs(e)
            i += 1
            if not flag:
                is_completed = True
    except Exception as e:
        print(str(e))
        saveLogs(e)


@start_new_thread
def load_all_job_scrappers():
    print()
    while AllSyncConfig.objects.filter(status=True).first() is not None:
        print("Load All Scraper Function")
        try:
            scrapers = get_scrapers_list('all')
            run_scrapers(scrapers)
        except Exception as e:
            print(e)
            saveLogs(e)
    print("Script Terminated")
    return True


# @shared_task()
@start_new_thread
def load_job_scrappers(job_source):
    job_source = job_source.lower()
    try:
        SchedulerSync.objects.filter(
            job_source=job_source, type='instant').update(running=True)
        scrapers = get_scrapers_list(job_source)
        run_scrapers(scrapers)
    except Exception as e:
        print(str(e))
        saveLogs(e)
    SchedulerSync.objects.all().update(running=False)
    return True


def run_scheduler(job_source):
    SchedulerSync.objects.filter(
        job_source=job_source, type="time/interval").update(running=True)
    # job_source = job_source.replace('_', '').lower()
    if job_source in list(scraper_functions.keys()):
        run_scrapers(get_scrapers_list(job_source))
    SchedulerSync.objects.filter(
        job_source=job_source, type="time/interval").update(running=False)


def start_job_sync(job_source):
    print("Interval Scheduler Started!")
    run_scheduler(job_source)
    print("Interval Scheduler Terminated!")


def start_background_job(job_source):
    print("Specific Time Scheduler Started")
    run_scheduler(job_source)
    print("Scheduler Terminated")


all_jobs_scheduler = BackgroundScheduler()
job_interval_scheduler = BackgroundScheduler()
job_time_scheduler = BackgroundScheduler()

linkedin_scheduler = BackgroundScheduler()
indeed_scheduler = BackgroundScheduler()
dice_scheduler = BackgroundScheduler()
career_builder_scheduler = BackgroundScheduler()
glassdoor_scheduler = BackgroundScheduler()
monster_scheduler = BackgroundScheduler()
zip_recruiter_scheduler = BackgroundScheduler()
adzuna_scheduler = BackgroundScheduler()
simply_hired_scheduler = BackgroundScheduler()
google_careers_scheduler = BackgroundScheduler()
jooble_scheduler = BackgroundScheduler()
talent_scheduler = BackgroundScheduler()
careerjet_scheduler = BackgroundScheduler()


def scheduler_settings():
    schedulers = SchedulerSettings.objects.filter(is_group=False)
    for scheduler in schedulers:
        if scheduler.interval_based:
            interval = convert_time_into_minutes(
                scheduler.interval, scheduler.interval_type)

            if scheduler.job_source.lower() == "linkedin":
                linkedin_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["linkedin"])

            elif scheduler.job_source.lower() == "indeed":
                indeed_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["indeed"])

            elif scheduler.job_source.lower() == "dice":
                dice_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["dice"])

            elif scheduler.job_source.lower().replace("_", "") == "careerbuilder":
                career_builder_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["career_builder"])

            elif scheduler.job_source.lower() == "glassdoor":
                glassdoor_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["glassdoor"])

            elif scheduler.job_source.lower() == "monster":
                monster_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["monster"])

            elif scheduler.job_source.lower() == "zip_recruiter":
                zip_recruiter_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["zip_recruiter"])

            elif scheduler.job_source.lower() == "simply_hired":
                simply_hired_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["simply_hired"])

            elif scheduler.job_source.lower() == "adzuna":
                adzuna_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["simply_hired"])

            elif scheduler.job_source.lower() == "google_careers":
                google_careers_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["google_careers"])

            elif scheduler.job_source.lower() == "jooble":
                jooble_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["jooble"])

            elif scheduler.job_source.lower() == "talent":
                talent_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["talent"])

            elif scheduler.job_source.lower() == "careerjet":
                careerjet_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["careerjet"])

        elif scheduler.time_based:
            now = datetime.datetime.now()
            dat = str(now).split(' ')
            start_time = dat[0] + " " + str(scheduler.time)
            if scheduler.job_source.lower() == "linkedin":
                linkedin_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                           args=["linkedin"])

            elif scheduler.job_source.lower() == "indeed":
                indeed_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                         args=["indeed"])

            elif scheduler.job_source.lower() == "dice":
                dice_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                       args=["dice"])

            elif scheduler.job_source.lower() == "career_builder":
                career_builder_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                                 args=["career_builder"])

            elif scheduler.job_source.lower() == "glassdoor":
                glassdoor_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                            args=["glassdoor"])

            elif scheduler.job_source.lower() == "monster":
                monster_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                          args=["monster"])

            elif scheduler.job_source.lower() == "simply_hired":
                simply_hired_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                               args=["simply_hired"])

            elif scheduler.job_source.lower() == "zip_recruiter":
                zip_recruiter_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                                args=["zip_recruiter"])

            elif scheduler.job_source.lower() == "adzuna_recruiter":
                adzuna_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                         args=["adzuna_recruiter"])

            elif scheduler.job_source.lower() == "google_careers":
                google_careers_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                                 args=["google_careers"])

            elif scheduler.job_source.lower() == "jooble":
                jooble_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                         args=["jooble"])

            elif scheduler.job_source.lower() == "talent":
                talent_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                         args=["talent"])

            elif scheduler.job_source.lower() == "careerjet":
                careerjet_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                            args=["careerjet"])


group_scraper_background_jobs = []
current_scraper = ''
current_group_scraper_id = None
current_group_scraper_running_time = ''


@start_new_thread
def group_scraper_job():
    global current_scraper
    global current_group_scraper_id
    global current_group_scraper_running_time
    last_scraper_running_time = current_group_scraper_running_time

    while True:
        if not current_group_scraper_id:
            continue
        try:
            group_scraper = GroupScraper.objects.get(
                pk=current_group_scraper_id)
            current_scraper = group_scraper.name
            last_scraper_running_time = current_group_scraper_running_time
        except Exception as e:
            print(str(e))
            saveLogs(e)
            continue

        try:
            print(f'starting group scraper - {group_scraper.name}')
            group_scraper_query = group_scraper.groupscraperquery
            if group_scraper_query:
                queries = group_scraper_query.queries
                new_scraper_started = False
                while not new_scraper_started:
                    for query in queries:
                        if last_scraper_running_time != current_group_scraper_running_time:
                            upload_jobs()
                            remove_files('all')
                            new_scraper_started = True
                            break
                        job_source = query['job_source'].lower()
                        print(job_source)
                        if job_source in list(single_scrapers_functions.keys()):
                            scraper_func = single_scrapers_functions[job_source]
                            try:
                                scraper_func(query['link'], query['job_type'])
                                upload_jobs()
                                remove_files(job_source)
                            except Exception as e:
                                print(e)
                                saveLogs(e)
        except Exception as e:
            upload_jobs()
            remove_files('all')
            current_scraper = ''
            print(str(e))
            saveLogs(e)


def change_group_scraper_id(group_id):
    global current_group_scraper_id
    global current_group_scraper_running_time
    current_group_scraper_id = group_id
    current_group_scraper_running_time = str(datetime.datetime.now())


def stop_group_scraper_jobs():
    print("Stopping group scrapper jobs ...")
    for job in group_scraper_background_jobs:
        job.shutdown()


def run_group_scraper_jobs():
    print("Running group scraper jobs ... ")

    for job in group_scraper_background_jobs:
        job.start()


def start_group_scraper_scheduler():
    stop_group_scraper_jobs()
    global group_scraper_background_jobs
    group_scraper_background_jobs = []
    group_scrapers = GroupScraper.objects.select_related()
    for group_scraper in group_scrapers:
        scheduler = group_scraper.scheduler_settings
        group_scraper_scheduler = BackgroundScheduler()
        if scheduler:
            if scheduler.interval_based:
                interval = convert_time_into_minutes(
                    scheduler.interval, scheduler.interval_type)
                group_scraper_scheduler.add_job(
                    change_group_scraper_id, 'interval', minutes=interval, args=[group_scraper.id])
                group_scraper_background_jobs.append(group_scraper_scheduler)
            elif scheduler.time_based:
                group_scraper_scheduler.add_job(change_group_scraper_id, 'cron',
                                                day_of_week='*' if not scheduler.week_days else scheduler.week_days,
                                                hour=scheduler.time.hour, minute=scheduler.time.minute,
                                                args=[group_scraper.id])
                group_scraper_background_jobs.append(group_scraper_scheduler)
    run_group_scraper_jobs()


# try:
#     if env("ENVIRONMENT") != "local":
#         start_group_scraper_scheduler()
#         group_scraper_job()
# except Exception as e:
#     print(e)


