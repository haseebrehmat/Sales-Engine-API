import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler
from job_portal.classifier import JobClassifier
from job_portal.data_parser.job_parser import JobParser
from job_portal.models import JobDetail
from job_scraper.jobs.careerbuilder_scraping import career_builder
from job_scraper.jobs.dice_scraping import dice
from job_scraper.jobs.glassdoor_scraping import glassdoor
from job_scraper.jobs.indeed_scraping import indeed
from job_scraper.jobs.jobs_create import linkedin_job_create, monster_job_create, glassdoor_job_create, \
    career_builder_job_create, dice_job_create, indeed_job_create
from job_scraper.jobs.linkedin_scraping import linkedin
from job_scraper.jobs.monster_scraping import monster
from job_scraper.models import SchedulerSettings
from job_scraper.models.scheduler import SchedulerSync
from job_scraper.utils.helpers import convert_time_into_minutes
from job_scraper.utils.thread import start_new_thread

scraper_functions = [
    linkedin,  # Tested working
    linkedin_job_create,
    indeed,  # Tested working
    indeed_job_create,
    dice,  # Tested working
    dice_job_create,
    career_builder,  # Tested working
    career_builder_job_create,
    glassdoor,  # Tested working
    glassdoor_job_create,
    monster,  # Tested working
    monster_job_create
]


def upload_jobs():
    path = 'job_scraper/job_data/'
    temp = os.listdir(path)
    files = [path + file for file in temp]

    job_parser = JobParser(files)
    # validate files first
    is_valid, message = job_parser.validate_file()

    try:
        job_parser.parse_file()
        upload_file(job_parser)
    except Exception as e:
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


@start_new_thread
def load_job_scrappers():
    for function in scraper_functions:
        try:
            function()
        except Exception as e:
            print(e)
    upload_jobs()
    queryset = SchedulerSync.objects.filter(running=True).first()
    queryset.running = False
    queryset.save()


def run_scheduler(job_source):
    if job_source == "linkedin":
        linkedin()
        linkedin_job_create()
    elif job_source == "indeed":
        indeed()
        indeed_job_create()
    elif job_source == "dice":
        dice()
        dice_job_create()
    elif job_source == "career_builder":
        career_builder()
        career_builder_job_create()
    elif job_source == "glassdoor":
        glassdoor()
        glassdoor_job_create()
    elif job_source == "monster":
        monster()
        monster_job_create()
    upload_jobs()


def start_job_sync(job_source):
    print("Interval Scheduler Started!")
    run_scheduler(job_source)
    print("Interval Scheduler Terminated!")
    job_interval_scheduler.pause()


def start_background_job(job_source):
    print("Specific Time Scheduler Started")
    run_scheduler(job_source)
    print("Scheduler Terminated")
    job_time_scheduler.pause()


all_jobs_scheduler = BackgroundScheduler()
job_interval_scheduler = BackgroundScheduler()
job_time_scheduler = BackgroundScheduler()

linkedin_scheduler = BackgroundScheduler()
indeed_scheduler = BackgroundScheduler()
dice_scheduler = BackgroundScheduler()
career_builder_scheduler = BackgroundScheduler()
glassdoor_scheduler = BackgroundScheduler()
monster_scheduler = BackgroundScheduler()


def scheduler_settings():
    schedulers = SchedulerSettings.objects.all()
    for scheduler in schedulers:
        if scheduler.interval_based:
            interval = convert_time_into_minutes(scheduler.interval, scheduler.interval_type)

            if scheduler.job_source.lower() == "linkedin":
                linkedin_scheduler.add_job(start_job_sync, 'interval', minutes=interval, args=["linkedin"])

            elif scheduler.job_source.lower() == "indeed":
                indeed_scheduler.add_job(start_job_sync, 'interval', minutes=interval, args=["indeed"])

            elif scheduler.job_source.lower() == "dice":
                dice_scheduler.add_job(start_job_sync, 'interval', minutes=interval, args=["dice"])

            elif scheduler.job_source.lower() == "career_builder":
                career_builder_scheduler.add_job(start_job_sync, 'interval', minutes=interval, args=["career_builder"])

            elif scheduler.job_source.lower() == "glassdoor":
                glassdoor_scheduler.add_job(start_job_sync, 'interval', minutes=interval, args=["glassdoor"])

            elif scheduler.job_source.lower() == "monster":
                monster_scheduler.add_job(start_job_sync, 'interval', minutes=interval, args=["monster"])

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


scheduler_settings()
