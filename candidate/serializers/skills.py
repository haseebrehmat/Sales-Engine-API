from rest_framework import serializers
from candidate.models import CandidateSkills
from candidate.models.skills import Skills


class CandidateSkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateSkills
        fields = "__all__"
        depth = 2


class SkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skills
        fields = "__all__"
        depth = 2
