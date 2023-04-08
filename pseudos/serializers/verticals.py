from rest_framework import serializers

from pseudos.models import Verticals


class VerticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verticals
        fields = "__all__"
