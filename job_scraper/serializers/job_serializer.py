from rest_framework import serializers

from job_scraper.models import Job

class JobSerializer(serializers.ModelSerializer):
  class Meta:
    model = Job
    fields = '__all__'
