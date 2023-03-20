from scraping.serializers.job_serializer import JobSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
import pandas as pd
import csv
import json

class JobView():
  def get(self):
    count = 0
    with open('scraping/linkedin_results.csv', newline='') as file:
      reader = csv.reader(file)

      for row in reader:
        if count != 0:
          file_data={
            "job_title":row[1],
            "company_name":row[2],
            "address":row[3],
            "job_description":row[4],
            "job_source_url":row[5],
            "job_posted_date":row[6],
          }

          job = JobSerializer(data=file_data)
          # import pdb
          # pdb.set_trace()
          print(count)
          job.is_valid(raise_exception=True)
          job.save()
        count += 1

    print(count)

    return HttpResponse(status=status.HTTP_200_OK)
