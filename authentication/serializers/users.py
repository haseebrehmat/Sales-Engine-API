from collections import OrderedDict

from rest_framework import serializers

from authentication.models import User
from authentication.models.team_management import TeamManagement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


    # def to_representation(self, instance):
    #     # Here instance is instance of your model
    #     # so you can build your dict however you like
    #     result = OrderedDict()
    #     result['status'] = instance.job.job_status
    #     result['job_id'] = instance.job.id
    #     return result