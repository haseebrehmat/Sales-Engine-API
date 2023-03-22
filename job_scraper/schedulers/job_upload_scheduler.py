import os
from threading import Thread

import pandas as pd
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

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
    print("oK")
    queryset = SchedulerSync.objects.first()
    queryset.running = True
    queryset.save()
    for x in scraper_functions:
        try:
            print("ok")
            x()
        except Exception as e:
            print(e)
    upload_jobs()
    queryset.running = False
    queryset.save()


def start_job_sync():
    job_time_scheduler.pause()
    print("Interval Scheduler Started!")
    load_job_scrappers()
    print("Interval Scheduler Terminated!")
    job_interval_scheduler.pause()


def start_background_job():
    job_interval_scheduler.pause()
    print("Specific Time Scheduler Started")
    load_job_scrappers()
    print("Scheduler Termintated")
    job_time_scheduler.pause()


all_jobs_scheduler = BackgroundScheduler()
job_interval_scheduler = BackgroundScheduler()
job_time_scheduler = BackgroundScheduler()

schedulers = SchedulerSettings.objects.all()
print("Schedulers", schedulers)

for scheduler in schedulers:
    if scheduler.interval:
        time_format = scheduler.interval_based
        interval = scheduler.interval

        job_interval_scheduler.add_job(start_job_sync, 'interval', minutes=scheduler.interval)
    elif scheduler.type == "time":
        job_time_scheduler.add_job(start_background_job, trigger=CronTrigger(start_date=scheduler.scheduler_time))
