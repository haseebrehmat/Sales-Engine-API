from rest_framework import serializers

from candidate.models import Designation


class DesignationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Designation
        fields = "__all__"
