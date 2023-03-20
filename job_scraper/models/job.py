from django.db import models
from utils.model_fields.timestamped import TimeStamped


class Job(TimeStamped):
  job_title = models.CharField(max_length=500)
  company_name = models.CharField(max_length=500)
  address = models.CharField(max_length=500)
  job_description = models.CharField(max_length=10000)
  job_source_url = models.CharField(max_length=5000)
  job_posted_date = models.CharField(max_length=70)

  def __str__(self):
    return self.job_title
