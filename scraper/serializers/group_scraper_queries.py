from rest_framework import serializers
from scraper.models import GroupScraperQuery


class GroupScraperQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupScraperQuery
        fields = '__all__'
        depth = 1
