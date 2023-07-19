from rest_framework import serializers

from authentication.models import UserRegions


class UserRegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegions
        fields = '__all__'