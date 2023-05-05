from rest_framework import serializers

from pseudos.models import SectionStatus


class SectionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionStatus
        fields = '__all__'
        depth = 1
