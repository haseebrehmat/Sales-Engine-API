from rest_framework import serializers
from job_portal.models import DownloadLogs


class DownloadLogsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(default={})

    class Meta:
        model = DownloadLogs
        fields = '__all__'

    def get_user(self, obj):
        return {
            'name': obj.user.username,
            'email': obj.user.email,
            'id': obj.user.id
        }
