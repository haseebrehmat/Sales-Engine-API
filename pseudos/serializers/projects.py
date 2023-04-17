from rest_framework import serializers

from pseudos.models import Projects


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = "__all__"
        # depth = 1
