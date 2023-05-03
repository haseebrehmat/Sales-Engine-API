from rest_framework import serializers

from pseudos.models import Skills, GenericSkills


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'
        depth = 1


class GenericSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericSkills
        fields = ["id", "name", "type"]
