from rest_framework import serializers
from job_scraper.models import JobSourceQuery


class JobQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSourceQuery
        fields = '__all__'
