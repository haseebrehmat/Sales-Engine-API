from rest_framework import serializers

from authentication.serializers.users import UserDetailSerializer
from job_portal.serializers.applied_job_serializer import AppliedJobStatusSerializer, AppliedJobStatusCustomSerializer
from lead_management.models import Lead, LeadActivity, LeadActivityNotes
from lead_management.serializers import CompanyStatusSerializer, LeadActivityNotesSerializer


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'
        depth = 1


class LeadDetailSerializer(serializers.ModelSerializer):
    # lead_activities = serializers.SerializerMethodField()
    applied_job_status = AppliedJobStatusCustomSerializer()
    company_status = CompanyStatusSerializer()
    notes = serializers.SerializerMethodField(default=[])

    class Meta:
        model = Lead
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lead_activity = LeadActivity.objects.filter(lead=instance, phase=instance.phase,
                                                    company_status=instance.company_status).first()
        representation['effect_date'] = lead_activity.effect_date if lead_activity else ''
        representation['due_date'] = lead_activity.due_date if lead_activity else ''
        return representation

    def get_notes(self, obj):
        lead_activities_ids = list(
            LeadActivity.objects.filter(lead=obj, company_status=obj.company_status, phase=obj.phase).values_list('id',
                                                                                                                  flat=True))
        queryset = LeadActivityNotes.objects.filter(lead_activity_id__in=lead_activities_ids)
        serializer = LeadActivityNotesSerializer(queryset, many=True)
        return serializer.data

    # def get_lead_activities(self, obj):
    #     queryset = LeadActivity.objects.filter(lead=obj)
    #     serializer = LeadActivitySerializer(queryset, many=True)
    #     return serializer.data
