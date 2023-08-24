from rest_framework import serializers

from authentication.models import User
from authentication.serializers.users import UserDetailSerializer, UserSerializer
from lead_management.models import LeadActivityNotes, LeadActivityNotesAttachment


class LeadActivityNotesSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = LeadActivityNotes
        fields = '__all__'
        depth = 1

    def get_attachments(self, obj):
        obj = LeadActivityNotesAttachment.objects.filter(lead_activity_notes=obj)
        if obj:
            obj = obj.first()
            return {'url': obj.attachment, 'filename': obj.filename}
        else:
            return None