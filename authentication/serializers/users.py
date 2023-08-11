from rest_framework import serializers

from authentication.models import User, Profile, UserRegions, Role, MultipleRoles
from authentication.models.team_management import TeamRoleVerticalAssignment


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'id']
        # depth = 1


class UserSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    regions = serializers.SerializerMethodField()
    # verticals = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

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

    def get_regions(self, obj):
        user_regions = UserRegions.objects.filter(user=obj)
        return [{'label': user_region.region.region, 'value': user_region.region.id} for user_region in user_regions]

    def get_roles(self, obj):
        team_id = self.context.get('team_id')
        data = []
        user_regions = UserRegions.objects.filter(user=obj)
        regions = [
            {
                'label': user_region.region.region,
                'value': user_region.region.id
            } for user_region in user_regions]
        try:
            ids = [obj.roles.id]
            ids.extend(MultipleRoles.objects.filter(user=obj).values_list("role_id", flat=True))
            if ids:
                qs = Role.objects.filter(id__in=set(ids))
                if qs:
                    serializer = RoleSerializer(qs, many=True)
                    data = serializer.data
                    count_roles = 0
                    for x in data:
                        team_roles = TeamRoleVerticalAssignment.objects.filter(role_id=x['id'], member_id=obj.id)
                        if team_id:
                            team_roles = team_roles.filter(team_id=team_id)
                        x["label"] = x["name"]
                        x["value"] = x["id"]
                        del x["name"]
                        del x['id']
                        x["verticals"] = [
                            {
                                "name": i.vertical.name,
                                "identity": i.vertical.identity,
                                "id": i.vertical.id,
                                "pseudo": i.vertical.pseudo.name,
                                "regions": regions
                            } for i in team_roles]

            return data
        except Exception as e:
            return data


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
