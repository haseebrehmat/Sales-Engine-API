from django.contrib.auth.models import Group, Permission
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"
        depth = 1

    @transaction.atomic
    def create(self, validated_data):
        permissions = validated_data.pop("permissions")

        group = Group.objects.create(**validated_data)
        for pemission_id in set(permissions):
            try:
                perm = Permission.objects.get(id=pemission_id)
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                raise ValidationError("Permission not found")

    @transaction.atomic
    def update(self, instance, validated_data):
        permissions = validated_data.pop("permissions")
        group = Group.objects.get(name=instance.name)
        group.permissions.clear()
        # group = Group.objects.create(**validated_data)
        for pemission_id in set(permissions):
            try:
                perm = Permission.objects.get(id=pemission_id)
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                raise ValidationError("Permission not found")
        group.name = validated_data.get("name", instance.name)
        group.save()
        return group





