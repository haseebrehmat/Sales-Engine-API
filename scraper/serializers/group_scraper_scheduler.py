from rest_framework import serializers

from scraper.models import GroupScraper


class GroupScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupScraper
        fields = '__all__'
        depth = 1
