from rest_framework import serializers

from authentication.models import User
from authentication.serializers.users import UserDetailSerializer, UserSerializer
from lead_management.models import LeadActivityNotes


class LeadActivityNotesSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = LeadActivityNotes
        fields = '__all__'
        depth = 1
