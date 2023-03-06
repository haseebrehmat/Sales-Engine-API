from rest_framework import serializers

from authentication.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["user"]
        depth = 1
