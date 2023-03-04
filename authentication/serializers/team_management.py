from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from rest_framework.permissions import IsAuthenticated

from settings.utils.helpers import serializer_errors

from authentication.models import Team, User
from rest_framework import serializers


class TeamManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"
        depth = 1

    def create(self, validated_data):
        members = validated_data.pop("members")
        reporting_to = validated_data.pop("reporting_to")
        team, is_created = Team.objects.update_or_create(**validated_data, reporting_to_id=reporting_to)
        members = User.objects.filter(id__in=members)
        team.members.clear()
        for member in members:
            team.members.add(member)
