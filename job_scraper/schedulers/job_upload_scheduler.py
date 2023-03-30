import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler
from job_portal.classifier import JobClassifier
from job_portal.data_parser.job_parser import JobParser
from job_portal.models import JobDetail
from job_scraper.jobs.adzuna_scraping import adzuna_scraping
from job_scraper.jobs.careerbuilder_scraping import career_builder
from job_scraper.jobs.dice_scraping import dice
from job_scraper.jobs.glassdoor_scraping import glassdoor
from job_scraper.jobs.indeed_scraping import indeed
from job_scraper.jobs.jobs_create import linkedin_job_create, monster_job_create, glassdoor_job_create, \
    career_builder_job_create, dice_job_create, indeed_job_create, simply_hired_job_create, zip_recruiter_job_create, \
    adzuna_job_create
from job_scraper.jobs.linkedin_scraping import linkedin
from job_scraper.jobs.monster_scraping import monster
from job_scraper.jobs.simply_hired_scraping import simply_hired
from job_scraper.jobs.ziprecruiter_scraping import ziprecruiter_scraping
from job_scraper.models import SchedulerSettings
from job_scraper.models.scheduler import SchedulerSync
from job_scraper.utils.helpers import convert_time_into_minutes
from job_scraper.utils.thread import start_new_thread

scraper_functions = {
    "linkedin": [
        linkedin,  # Tested working
        linkedin_job_create,
    ],
    "indeed": [
        indeed,  # Tested working
        indeed_job_create,
    ],
    "dice": [
        dice,  # Tested working
        dice_job_create,
    ],
    "careerbuilder": [
        career_builder,  # Test working
        career_builder_job_create,
    ],
    "glassdoor": [
        glassdoor,  # Tested working
        glassdoor_job_create,
    ],
    "monster": [
        monster,  # Tested working
        monster_job_create,
    ],
    "simplyhired": [
        simply_hired,  # Tested working
        simply_hired_job_create,
    ],
    "ziprecruiter": [
        ziprecruiter_scraping,  # not working
        zip_recruiter_job_create,
    ],
    "adzuna": [
        adzuna_scraping,
        adzuna_job_create
    ]
}


def upload_jobs():
    try:
        path = 'job_scraper/job_data/'
        temp = os.listdir(path)
        files = [path + file for file in temp]
        job_parser = JobParser(files)
        # validate files first
        is_valid, message = job_parser.validate_file()
        if is_valid:
            job_parser.parse_file()
            upload_file(job_parser)
    except Exception as e:
        print(e)


def remove_files():
    try:
        folder_path = 'job_scraper/job_data'
        files = os.listdir(folder_path)

        # Loop through the files and remove each one
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            try:
                os.remove(file_path)
                print(f"Removed {file_path}")
            except Exception as e:
                print(f"Failed to remove {file_path}. Error: {str(e)}")
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
def load_job_scrappers(job_source):
    try:
        SchedulerSync.objects.filter(job_source=job_source).update(running=True)
        if job_source != "all":
            functions = scraper_functions[job_source]
        else:
            scrapers = [scraper_functions[key] for key in list(scraper_functions.keys())]
            functions = []
            for function in scrapers:
                functions.extend(function)

        for function in functions:
            try:
                function()
            except Exception as e:
                print(e)
            try:
                upload_jobs()
            except Exception as e:
                print("Error in uploading jobs", e)
            remove_files()
    except Exception as e:
        print(e)
    SchedulerSync.objects.all().update(running=False)

    return True


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
    elif job_source == "zip_recruiter":
        ziprecruiter_scraping()
        zip_recruiter_job_create()
    elif job_source == "simply_hired":
        simply_hired()
        simply_hired_job_create()
    elif job_source == "adzuna":
        adzuna_scraping()
        adzuna_job_create()

    upload_jobs()


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

            elif scheduler.job_source.lower().replace("_", "") == "careerbuilder":
                career_builder_scheduler.add_job(start_job_sync, 'interval', minutes=interval, args=["career_builder"])

            elif scheduler.job_source.lower() == "glassdoor":
                glassdoor_scheduler.add_job(start_job_sync, 'interval', minutes=interval, args=["glassdoor"])

            elif scheduler.job_source.lower() == "monster":
                monster_scheduler.add_job(start_job_sync, 'interval', minutes=interval, args=["monster"])

            elif scheduler.job_source.lower() == "zip_recruiter":
                zip_recruiter_scheduler.add_job(start_job_sync, 'interval', minutes=interval, args=["zip_recruiter"])

            elif scheduler.job_source.lower() == "simply_hired":
                simply_hired_scheduler.add_job(start_job_sync, 'interval', minutes=interval, args=["simply_hired"])

            elif scheduler.job_source.lower() == "adzuna":
                adzuna_scheduler.add_job(start_job_sync, 'interval', minutes=interval, args=["simply_hired"])

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


# scheduler_settings()
