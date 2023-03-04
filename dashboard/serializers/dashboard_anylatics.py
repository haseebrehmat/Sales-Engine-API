import json
from collections import OrderedDict

from rest_framework import serializers

from job_portal.models import JobDetail


class LinkSerializer(serializers.Serializer):
    next = serializers.CharField(max_length=500)
    previous = serializers.CharField(max_length=500)


class DashboardStatisticsSerializer(serializers.Serializer):
    total = serializers.IntegerField(default=0)
    prospects = serializers.IntegerField(default=0)
    warm = serializers.IntegerField(default=0)
    cold = serializers.IntegerField(default=0)
    hired = serializers.IntegerField(default=0)
    rejected = serializers.IntegerField(default=0)


class DashboardLeadSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=0)
    name = serializers.CharField(max_length=500)
    total = serializers.IntegerField(default=0)
    prospects = serializers.IntegerField(default=0)
    warm = serializers.IntegerField(default=0),
    cold = serializers.IntegerField(default=0),
    hired = serializers.IntegerField(default=0),
    rejected = serializers.IntegerField(default=0)


class DashboardWeeklyLeadSerializer(serializers.Serializer):
    week_date = serializers.DateField(
        required=False, allow_null=True,
        format="%d-%m-%Y",
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
    )
    total = serializers.IntegerField(default=0)


class DashboardAnalyticsSerializer(serializers.Serializer):
    statistics = DashboardStatisticsSerializer()
    leads = DashboardLeadSerializer(many=True, source='*')
    weekly_leads = DashboardWeeklyLeadSerializer(many=True, source='*')

    class Meta:
        fields = ['statistics', 'leads', 'weekly_leads']
