from rest_framework import serializers

from job_portal.models import AppliedJobStatus


class AppliedJobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedJobStatus
        fields = "__all__"
        depth = 1


