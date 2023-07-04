from rest_framework import serializers
from django.db import transaction
from authentication.models import CustomPermission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPermission
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        print("Entered in create function")
        permissions = validated_data.pop("permissions")
        data = [CustomPermission(module=permission["module"], codename=permission["codename"], name=permission["name"], level=permission["name"]) for permission in
                permissions]
        CustomPermission.objects.bulk_create(data, ignore_conflicts=True)
        return True
