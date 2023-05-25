from rest_framework import serializers

from candidate.models import ExposedCandidate


class ExposedCandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExposedCandidate
        fields = "__all__"
        depth = 2
