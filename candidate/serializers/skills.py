from rest_framework import serializers
from candidate.models import CandidateSkills
from candidate.models import Skills


class CandidateSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateSkills
        fields = "__all__"


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"
