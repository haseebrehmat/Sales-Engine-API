from rest_framework import serializers

from candidate.models import Candidate, CandidateSkills
from candidate.serializers.skills import CandidateSkillsSerializer


class CandidateSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField(default=[])

    class Meta:
        model = Candidate
        fields = "__all__"
        depth = 1

    def get_skills(self, obj):
        queryset = CandidateSkills.objects.filter(candidate=obj)
        data = []
        if len(queryset) > 0:
            serializer_data = CandidateSkillsSerializer(queryset, many=True)
            data = serializer_data.data
        return data

