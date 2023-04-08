from rest_framework import serializers

from job_scraper.models import ScraperLogs


class ScraperLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScraperLogs
        fields = '__all__'
