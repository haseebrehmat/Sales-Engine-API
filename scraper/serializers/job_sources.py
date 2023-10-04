from rest_framework import serializers

from scraper.models import JobSource


class JobSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSource
        fields = '__all__'
