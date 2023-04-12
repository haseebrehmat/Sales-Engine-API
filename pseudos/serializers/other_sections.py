from rest_framework import serializers

from pseudos.models import OtherSection


class OtherSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherSection
        fields = "__all__"
        # depth = 1
