from rest_framework import serializers

from scraper.models import GroupScraper, GroupScraperQuery
from scraper.serializers.group_scraper_queries import GroupScraperQuerySerializer
from scraper.serializers.scheduler_settings import SchedulerSerializer


class GroupScraperSerializer(serializers.ModelSerializer):
    scheduler_settings = SchedulerSerializer()

    class Meta:
        model = GroupScraper
        fields = '__all__'
        depth = 1


