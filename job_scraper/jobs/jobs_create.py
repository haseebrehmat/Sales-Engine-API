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
        data={
          "job_title":col[1],
          "company_name":col[2],
          "address":col[3],
          "job_description":col[4],
          "job_source_url":col[5],
          "job_posted_date":col[6],
        }

        job_serializing(data)
      else:
        count += 1

def linkedin_job_create():
  file_read(LINKEDIN_CSV)

def indeed_job_create():
  file_read(INDEED_CSV)

def dice_job_create():
  file_read(DICE_CSV)

def career_builder_job_create():
  file_read(CAREER_BUILDER_CSV)

def glassdoor_job_create():
  file_read(GLASSDOOR_CSV)

def monster_job_create():
  file_read(MONSTER_CSV)
