from rest_framework import serializers

from scraper.models import SchedulerSync


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchedulerSync
        fields = '__all__'
