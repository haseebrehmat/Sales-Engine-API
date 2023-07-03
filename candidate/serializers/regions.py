from rest_framework import serializers

from candidate.models import Regions


class RegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = '__all__'
