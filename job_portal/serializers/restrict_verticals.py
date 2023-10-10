from rest_framework import serializers
from job_portal.models import RestrictVertical

class RestrictVerticalSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestrictVertical
        fields = "__all__"
