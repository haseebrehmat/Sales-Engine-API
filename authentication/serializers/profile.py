from rest_framework import serializers

from authentication.models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(default=[])

    class Meta:
        model = Profile
        exclude = ["company"]
        depth = 1

    def get_user(self, obj):
        queryset = User.objects.filter(id=obj.user.id).first()
        data = {
            "username": queryset.username,
            "email": queryset.email,
            "last_login": queryset.last_login,
        }
        return data

    def update(self, instance, validated_data):
        email = validated_data.pop("email")
        username = validated_data.pop("username")
        instance.first_name = validated_data.get("first_name")
        instance.last_name = validated_data.get("last_name")
        User.objects.filter(id=instance.user.id).update(email=email, username=username)
        instance.save()
        return instance
