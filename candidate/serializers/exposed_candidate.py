from rest_framework import serializers

from candidate.models import ExposedCandidate


class ExposedCandidateSerializer(serializers.ModelSerializer):
    candidate_id = serializers.IntegerField(default=None, read_only=False, write_only=True)
    company_id = serializers.UUIDField(default=None, read_only=False, write_only=True)

    class Meta:
        model = ExposedCandidate
        fields = "__all__"
        depth = 1


