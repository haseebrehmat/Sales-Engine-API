from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from job_scraper.jobs.careerbuilder_scraping import career_builder
from job_scraper.jobs.dice_scraping import dice
from job_scraper.jobs.glassdoor_scraping import glassdoor
from job_scraper.jobs.indeed_scraping import indeed
from job_scraper.jobs.jobs_create import linkedin_job_create, monster_job_create, glassdoor_job_create, \
    career_builder_job_create, dice_job_create, indeed_job_create
from job_scraper.jobs.linkedin_scraping import linkedin
from job_scraper.jobs.monster_scraping import monster

scraper_functions = [
    # linkedin,   # Facing credential issues
    # linkedin_job_create,
    indeed, # Tested working
    indeed_job_create,
    dice,   # Tested working
    dice_job_create,
    career_builder,   # Tested working
    career_builder_job_create,
    glassdoor,  # Tested working
    glassdoor_job_create,
    monster,    # Tested working
    monster_job_create
]

def start_job_sync():
    job_time_scheduler.pause()
    print("Interval Scheduler Started!")
    for x in scraper_functions:
        try:
            print("ok")
            x()
        except Exception as e:
            print(e)
    print("Interval Scheduler Terminated!")
    job_interval_scheduler.pause()


def start_background_job():
    job_interval_scheduler.pause()
    print("Specific Time Scheduler Started")
    for x in scraper_functions:
        try:
            print("ok")
            x()
        except Exception as e:
            print(e)
    print("Scheduler Termintated")
    job_time_scheduler.pause()

job_interval_scheduler = BackgroundScheduler()
job_time_scheduler = BackgroundScheduler()

start_date = datetime.now()
job_interval_scheduler.add_job(start_job_sync, 'interval', minutes=1, id="job_scheduler")
job_time_scheduler.add_job(start_background_job, id="job_2", trigger=CronTrigger(start_date=start_date))




