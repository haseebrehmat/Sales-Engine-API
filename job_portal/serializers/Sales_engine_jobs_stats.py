from rest_framework import serializers

from job_portal.models import SalesEngineJobsStats


class SalesEngineJobsStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesEngineJobsStats
        fields = '__all__'
