from rest_framework import serializers

from pseudos.models import Skills


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ["id", "name", "level"]
        # depth = 1
