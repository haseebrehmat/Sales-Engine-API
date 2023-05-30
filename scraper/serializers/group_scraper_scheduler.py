from rest_framework import serializers

from scraper.models import GroupScraper, GroupScraperQuery
from scraper.serializers.group_scraper_queries import GroupScraperQuerySerializer


class GroupScraperSerializer(serializers.ModelSerializer):
    queries = serializers.SerializerMethodField(default=[])

    class Meta:
        model = GroupScraper
        fields = '__all__'
        depth = 1

    def get_queries(self, obj):
        queryset = GroupScraperQuery.objects.filter(group_scraper=obj).first()
        return queryset.queries if queryset else []