from rest_framework import serializers


class JobCompanySerializer(serializers.Serializer):
    company = serializers.CharField(max_length=256)
    is_block = serializers.BooleanField()
