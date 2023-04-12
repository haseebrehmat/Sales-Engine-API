from rest_framework import serializers
from .models import Log

class LogSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


