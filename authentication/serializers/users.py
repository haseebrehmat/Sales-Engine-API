from rest_framework import serializers

from authentication.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()

    # verticals = serializers.SerializerMethodField()

    class Meta:
        model = User
        # fields = ["id", "username", "email"]
        exclude = ["is_superuser", "password", "last_login", "is_admin", "is_staff", "user_permissions"]
        depth = 1

    def get_company(self, obj):
        try:
            company = obj.profile.company
            company = {
                "id": company.id,
                "name": company.name
            }
        except:
            company = None
        return company

    # def get_verticals(self, obj):
    #     try:
    #         verticals = obj.profile.vertical.all()
    #         verticals = [{
    #             "id": vertical.id,
    #             "name": vertical.name,
    #             "identity": vertical.identity,
    #         } for vertical in verticals]
    #         return verticals
    #     except Exception as e:
    #         print("Exception in user serializer => ", str(e))
    #         return []


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        profile = Profile.objects.filter(user=instance).first()
        first_name = profile.first_name if profile.first_name else ''
        last_name = profile.last_name if profile.last_name else ''
        representation['name'] = f'{first_name} {last_name}'.strip()
        representation['avatar'] = profile.file_url
        return representation
