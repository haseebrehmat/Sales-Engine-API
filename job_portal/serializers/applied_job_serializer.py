from rest_framework import serializers

from authentication.serializers.users import UserDetailSerializer
from job_portal.models import AppliedJobStatus
from pseudos.serializers.verticals import VerticalSerializer


class AppliedJobStatusSerializer(serializers.ModelSerializer):
    applied_by = UserDetailSerializer()
    class Meta:
        model = AppliedJobStatus
        fields = "__all__"
        depth = 1


class AppliedJobStatusCustomSerializer(serializers.ModelSerializer):
    applied_by = UserDetailSerializer()
    vertical = VerticalSerializer()
    class Meta:
        model = AppliedJobStatus
        fields = "__all__"
        depth = 1


