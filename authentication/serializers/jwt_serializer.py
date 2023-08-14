from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.models import Role, MultipleRoles


class JwtSerializer(TokenObtainPairSerializer):
    """
    Adding additional parameters in jwt authentication token
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        try:
            token['permissions'] = list(user.roles.permissions.values_list('codename', flat=True))
        except:
            token["permissions"] = None

        try:
            token['role'] = user.roles.name
            token['role_id'] = str(user.roles.id)
        except:
            token['role'] = None
            token['role_id'] = None

        try:
            roles = MultipleRoles.objects.filter(user=user)
            token['roles'] = [{"id": str(x.role.id), "name": x.role.name} for x in roles]
        except:
            token['roles'] = None

        token['username'] = user.username

        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        try:
            token['company'] = str(user.profile.company.id)
            token['profile_image'] = str(user.profile.file_url)
        except:
            token["company"] = None
            token['profile_image'] = ""

        return token

