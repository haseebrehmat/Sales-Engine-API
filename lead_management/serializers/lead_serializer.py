from rest_framework import serializers

from job_portal.serializers.applied_job_serializer import AppliedJobStatusSerializer
from lead_management.models import Lead, LeadActivity, LeadActivityNotes
from lead_management.serializers import LeadActivitySerializer, CompanyStatusSerializer, LeadActivityNotesSerializer


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'
        depth = 1


class LeadDetailSerializer(serializers.ModelSerializer):
    # lead_activities = serializers.SerializerMethodField()
    applied_job_status = AppliedJobStatusSerializer()
    company_status = CompanyStatusSerializer()
    notes = serializers.SerializerMethodField(default=[])
    class Meta:
        model = Lead
        fields = '__all__'
        depth = 1

    def get_notes(self, obj):
        lead_activities_ids = list(LeadActivity.objects.filter(lead=obj, company_status=obj.company_status, phase=obj.phase).values_list('id', flat=True))
        queryset = LeadActivityNotes.objects.filter(lead_activity_id__in=lead_activities_ids)
        serializer = LeadActivityNotesSerializer(queryset, many=True)
        return serializer.data

    # def get_lead_activities(self, obj):
    #     queryset = LeadActivity.objects.filter(lead=obj)
    #     serializer = LeadActivitySerializer(queryset, many=True)
    #     return serializer.data
