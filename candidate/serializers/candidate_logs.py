from rest_framework import serializers

from candidate.models import CandidateLogs


class CandidateLogsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateLogs
        fields = "__all__"
