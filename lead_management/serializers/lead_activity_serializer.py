from rest_framework import serializers

from lead_management.models import LeadActivity, LeadActivityNotes
from lead_management.serializers import LeadActivityNotesSerializer


class LeadActivitySerializer(serializers.ModelSerializer):
    notes = serializers.SerializerMethodField(default=[])
    class Meta:
        model = LeadActivity
        fields = '__all__'
        depth=1

    def get_notes(self, instance):
        queryset = LeadActivityNotes.objects.filter(lead_activity=instance)
        serializer = LeadActivityNotesSerializer(queryset, many=True)
        return serializer.data
