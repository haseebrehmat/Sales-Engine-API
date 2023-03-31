from job_scraper.serializers.job_serializer import JobSerializer
from job_scraper.constants.const import *

import csv


def job_serializing(file_data):
    job = JobSerializer(data=file_data)
    job.is_valid(raise_exception=True)
    job.save()


def file_read(file_name):
    count = 0
    with open(file_name, newline='') as file:
        reader = csv.reader(file)

        for col in reader:
            if count != 0:
                data = {
                    "job_title": col[1],
                    "company_name": col[2],
                    "address": col[3],
                    "job_description": col[4],
                    "job_source_url": col[5],
                    "job_posted_date": col[6],
                }

                job_serializing(data)
            else:
                count += 1


def linkedin_job_create():
    try:
        file_read(LINKEDIN_CSV)
    except:
        print("File Not Found")


def indeed_job_create():
    try:
        file_read(INDEED_CSV)
    except:
        print("File Not Found")


def dice_job_create():
    try:
        file_read(DICE_CSV)
    except:
        print("File Not Found")


def career_builder_job_create():
    try:
        file_read(CAREER_BUILDER_CSV)
    except:
        print("File Not Found")


def glassdoor_job_create():
    try:
        file_read(GLASSDOOR_CSV)
    except:
        print("File Not Found")


def monster_job_create():
    try:
        file_read(MONSTER_CSV)
    except:
        print("File Not Found")


def simply_hired_job_create():
    try:
        file_read(SIMPLYHIREDCSV)
    except:
        print("File Not Found")


def zip_recruiter_job_create():
    try:
        file_read(ZIP_RECRUITER_CSV)
    except:
        print("File Not Found")


def adzuna_job_create():
    try:
        file_read(ADZUNA_CSV)
    except:
        print("File Not Found")
