from rest_framework import serializers

from scraper.models import SchedulerSettings


class SchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchedulerSettings
        fields = '__all__'
