from rest_framework import serializers

from pseudos.models.cover_letter import CoverLetter


class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = "__all__"
        # depth = 1
