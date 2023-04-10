from rest_framework import serializers

from pseudos.models import Experience


class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = "__all__"
