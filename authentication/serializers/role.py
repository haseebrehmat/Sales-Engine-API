from authentication.models import CustomPermission
from rest_framework import serializers

from authentication.models.company import Company
from authentication.models.role import Role
from django.forms.models import model_to_dict


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        depth = 1

    # def to_representation(self, instance):
    #     return list(instance.permissions)

    def create(self, validated_data):
        permissions = validated_data.pop("permissions")
        validated_data['company_id'] = str(self.context.user.profile.company.id)
        role = Role.objects.create(**validated_data)
        permissions = CustomPermission.objects.filter(codename__in=permissions)
        for permission in permissions:
            role.permissions.add(permission)

    def update(self, instance, validated_data):
        permissions = validated_data.pop("permissions")
        role = Role.objects.filter(pk=instance.id).update(**validated_data)
        permissions = CustomPermission.objects.filter(codename__in=permissions)
        instance.permissions.clear()
        for permission in permissions:
            instance.permissions.add(permission)
        return instance


class JobKeywordSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    count = serializers.IntegerField(default=0)


class PermissionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    code_name = serializers.CharField(max_length=500)
