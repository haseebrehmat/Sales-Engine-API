from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from rest_framework.permissions import IsAuthenticated

from authentication.serializers.users import UserSerializer
from pseudos.serializers.verticals import VerticalSerializer
from settings.utils.helpers import serializer_errors

from authentication.models import Team, User, Profile
from rest_framework import serializers


class TeamManagementSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = "__all__"
        depth = 3

    def get_members(self, obj):
        serializer = UserSerializer(obj.members.all(), many=True, context={"team_id": obj.id})

        return serializer.data

    def create(self, validated_data):
        members = validated_data.pop("members")
        reporting_to = validated_data.pop("reporting_to")
        team, is_created = Team.objects.update_or_create(**validated_data, reporting_to_id=reporting_to)
        members = User.objects.filter(id__in=members)
        team.members.clear()
        for member in members:
            team.members.add(member)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name")
        members = validated_data.get("members")
        instance.reporting_to_id = validated_data.get("reporting_to")
        members = User.objects.filter(id__in=members)
        instance.members.clear()
        for member in members:
            instance.members.add(member)
        instance.save()
        return instance


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['verticals'] = VerticalSerializer(instance.verticals.all(), many=True).data
        return representation