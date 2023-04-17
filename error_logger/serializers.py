from rest_framework import serializers
from .models import Log
from authentication.serializers.users import UserSerializer
class LogSerialzer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Log
        fields = '__all__'


