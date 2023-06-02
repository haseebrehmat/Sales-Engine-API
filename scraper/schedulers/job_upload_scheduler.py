import datetime
import os
import traceback

import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler

from job_portal.classifier import JobClassifier
from job_portal.data_parser.job_parser import JobParser
from job_portal.models import JobDetail
from scraper.jobs import single_scrapers_functions
from scraper.jobs.adzuna_scraping import adzuna_scraping
from scraper.jobs.careerbuilder_scraping import career_builder
from scraper.jobs.dice_scraping import dice
from scraper.jobs.glassdoor_scraping import glassdoor
from scraper.jobs.google_careers_scraping import google_careers
from scraper.jobs.indeed_scraping import indeed
from scraper.jobs.jooble_scraping import jooble
from scraper.jobs.linkedin_scraping import linkedin
from scraper.jobs.monster_scraping import monster
from scraper.jobs.simply_hired_scraping import simply_hired
from scraper.jobs.ziprecruiter_scraping import ziprecruiter_scraping
from scraper.models import JobSourceQuery, GroupScraper
from scraper.models import SchedulerSettings, AllSyncConfig
from scraper.models.scheduler import SchedulerSync
from scraper.utils.helpers import convert_time_into_minutes
from scraper.utils.thread import start_new_thread
from utils.helpers import saveLogs

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
    ]
}


def upload_jobs():
    try:
        print("Start uploading files ... ")
        path = 'scraper/job_data/'
        temp = os.listdir(path)
        files = [path + file for file in temp]
        valid_files = [file for file in files if not is_file_empty(file)]
        if valid_files:
            job_parser = JobParser(valid_files)
            # validate files first
            is_valid, message = job_parser.validate_file()
            if is_valid:
                job_parser.parse_file()
            upload_file(job_parser)
            print("File uploaded successfully!")
        else:
            print("No valid files for uploading.")
    except Exception as e:
        print(
            f"An exception occurred: {e}\n\nTraceback: {traceback.format_exc()}")
        saveLogs(e)


def is_file_empty(file):
    try:
        valid_extensions = ['.csv', '.xlsx', '.ods', 'odf', '.odt']
        if isinstance(file, str):
            ext = ".csv"
        else:
            ext = os.path.splitext(file.name)[1]
        df = pd.read_csv(
            file, engine='c', nrows=1) if ext == '.csv' else pd.read_excel(file, nrows=1)
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


def upload_file(job_parser):
    # parse, classify and upload data to database
    classify_data = JobClassifier(job_parser.data_frame)
    classify_data.classify()

    model_instances = [
        JobDetail(
            job_title=job_item.job_title,
            company_name=job_item.company_name,
            job_source=job_item.job_source,
            job_type=job_item.job_type,
            address=job_item.address,
            job_description=job_item.job_description,
            tech_keywords=job_item.tech_keywords.replace(" / ", "").lower(),
            job_posted_date=job_item.job_posted_date,
            job_source_url=job_item.job_source_url,
        ) for job_item in classify_data.data_frame.itertuples()]

    JobDetail.objects.bulk_create(
        model_instances, ignore_conflicts=True, batch_size=1000)


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
    scrapers_without_links = [
        'adzuna', 'googlecareers', 'ziprecruiter']
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
                        if key in scrapers_without_links:
                            scraper_function()
                            scraper['stop_status'] = True
                            flag = True
                        else:
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


# scheduler_settings()

group_scraper_background_jobs = []
current_scraper = ''


def group_scraper_job(group_scraper):
    global current_scraper
    if group_scraper.name != current_scraper:
        current_scraper = group_scraper.name
    try:
        print(f'starting group scraper - {group_scraper.name}')
        group_scraper_query = group_scraper.groupscraperquery
        if group_scraper_query:
            queries = group_scraper_query.queries
            for query in queries:
                if current_scraper != '' and current_scraper != group_scraper.name:
                    upload_jobs()
                    return
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
        print(str(e))
        saveLogs(e)


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
                    group_scraper_job, 'interval', minutes=interval, args=[group_scraper])
                group_scraper_background_jobs.append(group_scraper_scheduler)
            elif scheduler.time_based:
                group_scraper_scheduler.add_job(group_scraper_job, 'cron',
                                                day_of_week='*' if not scheduler.week_days else scheduler.week_days,
                                                hour=scheduler.time.hour, minute=scheduler.time.minute,
                                                args=[group_scraper])
                group_scraper_background_jobs.append(group_scraper_scheduler)
    run_group_scraper_jobs()


@start_new_thread
def run_group_scraper_scheduler_job():
    group_scrapers = GroupScraper.objects.all()
    for group_scraper in group_scrapers:
        group_scraper_job(group_scraper)


try:
    start_group_scraper_scheduler()
    run_group_scraper_scheduler_job()
except Exception as e:
    print(e)
