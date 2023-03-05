from rest_framework import serializers

from job_portal.models import BlacklistJobs


class BlacklistSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlacklistJobs
        fields = "__all__"

