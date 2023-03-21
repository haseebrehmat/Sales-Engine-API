from rest_framework import serializers

from job_scraper.models import SchedulerSync


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchedulerSync
        fields = '__all__'
