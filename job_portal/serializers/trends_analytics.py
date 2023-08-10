from rest_framework import serializers

from job_portal.models import TrendsAnalytics


class TrendsAnalyticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrendsAnalytics
        fields = '__all__'
