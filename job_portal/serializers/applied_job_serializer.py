from rest_framework import serializers

from authentication.serializers.users import UserDetailSerializer
from job_portal.models import AppliedJobStatus


class AppliedJobStatusSerializer(serializers.ModelSerializer):
    applied_by = UserDetailSerializer()

    class Meta:
        model = AppliedJobStatus
        fields = "__all__"
        depth = 1


