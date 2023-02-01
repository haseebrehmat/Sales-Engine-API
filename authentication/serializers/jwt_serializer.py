from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class JwtSerializer(TokenObtainPairSerializer):
    """
    Adding additional parameters in jwt authentication token
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['permissions'] = list(user.get_group_permissions())
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff

        return token
