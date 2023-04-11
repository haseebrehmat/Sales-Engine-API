from rest_framework import serializers

from pseudos.models import Links


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = "__all__"
