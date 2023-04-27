from rest_framework import serializers

from scraper.models import ScraperLogs


class ScraperLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScraperLogs
        fields = '__all__'
