from rest_framework import serializers

from pseudos.models import Certificate
from pseudos.models.configurations import VerticalConfigurations


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerticalConfigurations
        fields = "__all__"
