import datetime
import json
import os
import time
from datetime import datetime
import traceback
import pytz
import pandas as pd
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.db import transaction
from django.db.models import Q
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from settings.base import env

from job_portal.classifier import JobClassifier
from job_portal.data_parser.job_parser import JobParser
from job_portal.models import JobDetail, JobUploadLogs, JobArchive, SalesEngineJobsStats
from scraper.jobs import single_scrapers_functions, working_nomads, dynamite, arc_dev, job_gether, receptix, the_muse, remote_co
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
from scraper.jobs.dailyremote_scraping import dailyremote
from scraper.jobs.talent_scraping import talent
from scraper.jobs.ziprecruiter_scraping import ziprecruiter_scraping
from scraper.jobs.recruit_scraping import recruit
from scraper.jobs.rubynow_scraping import rubynow
from scraper.jobs.ycombinator_scraping import ycombinator
from scraper.jobs.workopolis_scraping import workopolis
from scraper.jobs.remote_ok_scraping import remoteok
from scraper.jobs.himalayas_scraping import himalayas
from scraper.jobs.us_jora_scraping import us_jora
from scraper.jobs.startwire_scraping import startwire
from scraper.jobs.start_up_scraping import startup
from scraper.jobs.builtin_scraping import builtin
from scraper.jobs.workable_scraping import workable
from scraper.jobs.hirenovice_scraping import hirenovice
from scraper.jobs.clearance_scraping import clearance
from scraper.jobs.smartrecruiter_scraping import smartrecruiter
from scraper.jobs.getwork_scraping import getwork
from scraper.jobs.ruby_on_remote_scraping import ruby_on_remote
from scraper.jobs.just_remote_scraping import just_remote
from scraper.jobs.linkedin_group_scraping import linkedin_group

from scraper.models import JobSourceQuery, ScraperLogs
from scraper.models.group_scraper import GroupScraper
from scraper.models.group_scraper_query import GroupScraperQuery
from scraper.jobs.hubstaff_talent_scraping import hubstaff_talent

from scraper.models import JobSourceQuery, GroupScraper, ScraperLogs
from scraper.models import SchedulerSettings, AllSyncConfig
from scraper.models.scheduler import SchedulerSync
from scraper.utils.helpers import convert_time_into_minutes
from scraper.utils.thread import start_new_thread
from settings.base import env
from utils import upload_to_s3
from utils.helpers import saveLogs
from utils.sales_engine import upload_jobs_in_sales_engine, upload_jobs_in_production
from django.utils import timezone

# from error_logger.models import Log
# from scraper.utils.thread import start_new_thread
from celery import shared_task
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
    "hirenovice": [
        hirenovice,
    ],
    "talent": [
        talent,
    ],
    "careerjet": [
        careerjet,
    ],
    "dailyremote": [
        dailyremote,
    ],
    "recruit": [
        recruit,
    ],
    "rubynow": [
        rubynow,
    ],
    "ycombinator": [
        ycombinator,
    ],
    "workingnomads": [
        working_nomads,
    ],
    "workopolis": [
        workopolis,
    ],
    "dynamite": [
        dynamite,
    ],
    "arcdev": [
        arc_dev,
    ],
    "remoteok": [
        remoteok,
    ],
    "himalayas": [
        himalayas,
    ],
    "usjora": [
        us_jora,
    ],
    "startwire": [
        startwire,
    ],
    "jobgether": [
        job_gether,
    ],
    "startup": [
        startup,
    ],
    "receptix": [
        receptix,
    ],
    "builtin": [
        builtin,
    ],
    "workable": [
        workable
    ],
    "themuse": [
        the_muse,
    ],
    "clearance": [
        clearance,
    ],
    "smartrecruiter": [
        smartrecruiter,
    ],
    "getwork": [
        getwork,
    ],
    "rubyonremote": [
        ruby_on_remote
    ],
    "hubstafftalent": [
        hubstaff_talent,
    ],
    "justremote": [
        just_remote,
    ],
     "remoteco": [
        remote_co,
    ],
     "linkedin_group": [
        linkedin_group,
    ],

}


def upload_jobs(scheduler_type, job_source):
    try:
        print('Uploading files ...')
        path = 'scraper/job_data/'
        temp = os.listdir(path)
        files = [path + file for file in temp]
        SchedulerSync.objects.filter(
            job_source=job_source, type=scheduler_type).update(uploading=True)
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
                print(
                    f"An exception occurred: {e}\n\nTraceback: {traceback.format_exc()}")
                saveLogs(e)
    except Exception as e:
        print(
            f"An exception occurred: {e}\n\nTraceback: {traceback.format_exc()}")
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


def remove_files(scheduler_type, job_source="all"):
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
    SchedulerSync.objects.filter(
        job_source=job_source, type=scheduler_type).update(uploading=False)


@transaction.atomic
def upload_file(job_parser, filename):
    # parse, classify and upload data to database
    classify_data = JobClassifier(job_parser.data_frame)
    classify_data.classify()
    before_uploading_jobs = JobDetail.objects.count()

    # migrate_jobs_to_archive(classify_data)

    model_instances = [
        JobDetail(job_title=job_item.job_title, company_name=job_item.company_name, job_source=job_item.job_source,
                  job_type=job_item.job_type, address=job_item.address, job_description=job_item.job_description,
                  job_description_tags=job_item.job_description_tags,
                  tech_keywords=job_item.tech_keywords.replace(
                      " / ", "").lower(),
                  tech_stacks=list(
                      set(job_item.tech_keywords.replace(" / ", "").lower().split(','))),
                  job_posted_date=job_item.job_posted_date,
                  job_source_url=job_item.job_source_url,
                  estimated_salary=job_item.estimated_salary,
                  salary_format=job_item.salary_format,
                  salary_min=job_item.salary_min,
                  salary_max=job_item.salary_max)
        for job_item in classify_data.data_frame.itertuples() if
        job_item.job_source_url != "" and isinstance(job_item.job_source_url,
                                                     str)]

    JobDetail.objects.bulk_create(
        model_instances, ignore_conflicts=True, batch_size=1000)
    if env("ENVIRONMENT") == "stagging" or env("ENVIRONMENT") == "development":
        upload_jobs_in_production(model_instances, filename)
    upload_jobs_in_sales_engine(model_instances, filename)
    after_uploading_jobs_count = JobDetail.objects.count()
    scraper_log = ScraperLogs.objects.filter(
        filename=filename, uploaded_jobs=0).first()
    if scraper_log:
        uploaded_count = after_uploading_jobs_count - before_uploading_jobs
        if uploaded_count > 0:
            scraper_log.uploaded_jobs = uploaded_count
            scraper_log.save()


def migrate_jobs_to_archive(classify_data=None):
    try:
        last_30_days = datetime.datetime.now() - datetime.timedelta(days=30)
        excluded_id = JobArchive.objects.only(
            "id").values_list("id", flat=True)
        fields = [
            'id',
            'job_title',
            'company_name',
            'job_source',
            'job_type',
            'address',
            'job_description',
            'tech_keywords',
            'job_posted_date',
            'job_source_url',
            'block',
            'is_manual',
            'created_at',
            'updated_at'
        ]

        if classify_data:
            query = Q()
            for item in classify_data.data_frame.itertuples():
                query |= Q(company_name=item.company_name,
                           job_title=item.job_title)

        jobs = JobDetail.objects.filter(
            created_at__lte=last_30_days, job_applied="not applied")
        qs = JobDetail.objects.exclude(id__in=set(excluded_id)).only(*fields)
        print(jobs.count())
        if classify_data:
            jobs.filter(query)
        bulk_data = [JobArchive(
            id=x.id,
            job_title=x.job_title,
            company_name=x.company_name,
            job_source=x.job_source,
            job_type=x.job_type,
            address=x.address,
            job_description=x.job_description,
            tech_keywords=x.tech_keywords,
            job_posted_date=x.job_posted_date,
            job_source_url=x.job_source_url,
            block=x.block,
            is_manual=x.is_manual,
            created_at=x.created_at,
            updated_at=x.updated_at
        ) for x in qs]

        JobArchive.objects.bulk_create(bulk_data, ignore_conflicts=True)
        jobs.delete()
    except Exception as e:
        print("Exception in migrating data => ", e)

# migrate_jobs_to_archive()


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
                    scrapers[job_source] = {
                        'stop_status': False, 'function': function[0], 'job_source_queries': query}
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
                    scrapers[key] = {
                        'stop_status': False, 'function': function[0], 'job_source_queries': query}
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
                        upload_jobs('instant', key)
                        remove_files('instant', key)
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
    SchedulerSync.objects.filter(job_source='linkedin_group', type='Infinite Scrapper').update(running=True,
                                                                                    start_time=timezone.now(),
                                                                                    end_time=None)
    while AllSyncConfig.objects.filter(status=True).first() is not None:
        print("Linkedin Group in load all jobs")
        try:
            group_query = GroupScraperQuery.objects.all()
            linkedin_group(group_query)
            upload_jobs('Infinite Scrapper', 'linkedin_group')
            remove_files('Infinite Scrapper', 'linkedin_group')
        except Exception as e:
            print(e)
            saveLogs(e)
    SchedulerSync.objects.filter(job_source='linkedin_group', type='Infinite Scrapper').update(running=False,
                                                                                    end_time=timezone.now())
    print("Script Terminated")
    return True


@shared_task
def run_scraper_by_celery(job_source):
    time.sleep(5)
    return job_source


@start_new_thread
def load_job_scrappers(job_source):
    job_source = job_source.lower()
    try:
        SchedulerSync.objects.filter(job_source=job_source, type='instant').update(running=True,
                                                                                   start_time=timezone.now(),
                                                                                   end_time=None)
        scrapers = get_scrapers_list(job_source)
        run_scrapers(scrapers)
    except Exception as e:
        print(str(e))
        saveLogs(e)
    SchedulerSync.objects.all().update(running=False)
    SchedulerSync.objects.filter(
        job_source=job_source, type='instant').update(end_time=timezone.now())
    return True


def run_scheduler(job_source):
    SchedulerSync.objects.filter(job_source=job_source, type="time/interval").update(running=True,
                                                                                     start_time=timezone.now(),
                                                                                     end_time=None)
    # job_source = job_source.replace('_', '').lower()
    if job_source in list(scraper_functions.keys()):
        run_scrapers(get_scrapers_list(job_source))
    SchedulerSync.objects.filter(job_source=job_source, type="time/interval").update(running=False,
                                                                                     end_time=timezone.now())


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
rubynow_scheduler = BackgroundScheduler()
workopolis_scheduler = BackgroundScheduler()
recruit_scheduler = BackgroundScheduler()
dynamite_scheduler = BackgroundScheduler()
arcdev_scheduler = BackgroundScheduler()
himalayas_scheduler = BackgroundScheduler()
us_jora_scheduler = BackgroundScheduler()
startwire_scheduler = BackgroundScheduler()
job_gether_scheduler = BackgroundScheduler()
receptix_scheduler = BackgroundScheduler()
the_muse_scheduler = BackgroundScheduler()
hirenovice_scheduler = BackgroundScheduler()


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

            elif scheduler.job_source.lower() == "hirenovice":
                hirenovice_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["hirenovice"])

            elif scheduler.job_source.lower() == "talent":
                talent_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["talent"])

            elif scheduler.job_source.lower() == "careerjet":
                careerjet_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["careerjet"])

            elif scheduler.job_source.lower() == "rubynow":
                rubynow_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["rubynow"])

            elif scheduler.job_source.lower() == "workopolis":
                workopolis_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["workopolis"])

            elif scheduler.job_source.lower() == "himalayas":
                himalayas_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["himalayas"])

            elif scheduler.job_source.lower() == "recruit":
                recruit_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["recruit"])

            elif scheduler.job_source.lower() == "dynamite":
                dynamite_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["dynamite"])

                recruit_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["recruit"])
            elif scheduler.job_source.lower() == "dynamite":
                dynamite_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["dynamite"])
            elif scheduler.job_source.lower() == "arcdev":
                arcdev_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["arcdev"])

            elif scheduler.job_source.lower() == "usjora":
                us_jora_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["usjora"])

            elif scheduler.job_source.lower() == "remoteok":
                rubynow_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["remoteok"])

            elif scheduler.job_source.lower() == "startwire":
                startwire_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["startwire"])
            elif scheduler.job_source.lower() == "hubstafftalent":
                startwire_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["hubstafftalent"])
            elif scheduler.job_source.lower() == "jobgether":
                job_gether_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["jobgether"])
            elif scheduler.job_source.lower() == "receptix":
                receptix_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["receptix"])
            elif scheduler.job_source.lower() == "receptix":
                receptix_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["justremote"])
            elif scheduler.job_source.lower() == "justremote":
                the_muse_scheduler.add_job(
                    start_job_sync, 'interval', minutes=interval, args=["themuse"])

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

            elif scheduler.job_source.lower() == "hirenovice":
                hirenovice_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                             args=["hirenovice"])

            elif scheduler.job_source.lower() == "hirenovice":
                hirenovice_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                             args=["hirenovice"])

            elif scheduler.job_source.lower() == "talent":
                talent_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                         args=["talent"])

            elif scheduler.job_source.lower() == "careerjet":
                careerjet_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                            args=["careerjet"])

            elif scheduler.job_source.lower() == "rubynow":
                rubynow_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                          args=["rubynow"])

            elif scheduler.job_source.lower() == "workopolis":
                workopolis_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                             args=["workopolis"])

            elif scheduler.job_source.lower() == "himalayas":
                himalayas_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                            args=["himalayas"])

            elif scheduler.job_source.lower() == "recruit":
                recruit_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                          args=["recruit"])

            elif scheduler.job_source.lower() == "dynamite":
                dynamite_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                           args=["dynamite"])

            elif scheduler.job_source.lower() == "arcdev":
                arcdev_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                         args=["arcdev"])

            elif scheduler.job_source.lower() == "usjora":
                us_jora_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                          args=["usjora"])

            elif scheduler.job_source.lower() == "remoteok":
                rubynow_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                          args=["remoteok"])

            elif scheduler.job_source.lower() == "startwire":
                startwire_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                            args=["startwire"])
            elif scheduler.job_source.lower() == "hubstafftalent":
                startwire_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                            args=["hubstafftalent"])
            elif scheduler.job_source.lower() == "jobgether":
                job_gether_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                             args=["jobgether"])
            elif scheduler.job_source.lower() == "receptix":
                receptix_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                           args=["receptix"])
            elif scheduler.job_source.lower() == "themuse":
                the_muse_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                           args=["themuse"])
            elif scheduler.job_source.lower() == "justremote":
                the_muse_scheduler.add_job(start_background_job, "interval", hours=24, next_run_time=start_time,
                                           args=["justremote"])


def group_scraper_job(group_id):
    pakistan_timezone = pytz.timezone('Asia/Karachi')
    current_scraper = ''
    current_group_scraper_id = group_id
    group_scraper = GroupScraper.objects.filter(
        pk=current_group_scraper_id).first()

    current_scraper = group_scraper.name
    print(f"This is the time of group : {current_scraper}")
    current_scraper = current_scraper.lower()

    SchedulerSync.objects.filter(
        type="group scraper").update(running=False, end_time=datetime.now(pakistan_timezone))
    SchedulerSync.objects.filter(
        job_source=current_scraper).update(running=True, start_time=datetime.now(pakistan_timezone),
                                           end_time=datetime.now(pakistan_timezone))

    try:
        queries = GroupScraperQuery.objects.filter(group_scraper_id=group_id)
        change_status = GroupScraperQuery.objects.filter(status='running').exclude(group_scraper_id=group_id)
        for query in change_status:
            query.status = "remaining"
            query.save()
        change_status = GroupScraperQuery.objects.filter(status='running', group_scraper_id=group_id)
        for query in change_status:
            query.status = "failed"
            query.save()

        if group_scraper.running_link is None:
            for query in queries:
                query.status = "remaining"
                query.start_time = str(datetime.now(pakistan_timezone))
                query.end_time = str(datetime.now(pakistan_timezone))
                query.save()
        for query in queries:
            job_source = query.job_source.lower()
            print(job_source)
            if job_source in list(single_scrapers_functions.keys()) and query.status == "remaining":
                scraper_func = single_scrapers_functions[job_source]
                try:
                    group_scraper.running_link = query
                    group_scraper.save()
                    # start time and status running
                    query.status = "running"
                    query.start_time = str(datetime.now(pakistan_timezone))
                    query.save()
                    scraper_func(query.link, query.job_type)
                    upload_jobs('group scraper', job_source)
                    remove_files('group scraper', job_source)
                    # end time and status successfully completed
                    query.status = "completed"
                    query.end_time = str(datetime.now(pakistan_timezone))
                    query.save()
                except Exception as e:
                    # end time and status of missed
                    query.status = "failed"
                    query.end_time = str(datetime.now(pakistan_timezone))
                    query.save()
                    print(e)
                    saveLogs(e)
            else:
                group_scraper.running_link = query
                group_scraper.save()
                if job_source not in list(single_scrapers_functions.keys()):
                    query.status = "failed"
                    query.start_time = str(datetime.now(pakistan_timezone))
                    query.end_time = str(datetime.now(pakistan_timezone))
                    query.save()
                print("")
        upload_jobs('group scraper', 'all')
        remove_files('group scraper', 'all')
    except Exception as e:
        upload_jobs('group scraper', 'all')
        remove_files('group scraper', 'all')
        current_scraper = ''
        print(str(e))
        saveLogs(e)
    SchedulerSync.objects.filter(
        job_source=current_scraper).update(running=False, end_time=datetime.now(pakistan_timezone))
    if len(GroupScraperQuery.objects.filter(group_scraper_id=group_id, status='remaining')) == 0:
        group_scraper.running_link = None
        group_scraper.save()
    print("Group Scraper is finished")
