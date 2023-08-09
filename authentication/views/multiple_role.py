import datetime
import uuid
import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import Role, User, TeamRoleVerticalAssignment
from settings.base import SIMPLE_JWT


class MultipleRoleManagement(APIView):

    def get(self, request):
        multiple_roles = []
        user_id = request.GET.get("user_id")
        team_id = request.GET.get("team_id")
        if user_id:
            qs = User.objects.filter(id=user_id).first()
            if qs:
                multiple_roles = qs.multiple_roles
        else:
            multiple_roles = self.request.user.multiple_roles
        if multiple_roles:
            # exclude team based assign roles from the view
            assign_roles = TeamRoleVerticalAssignment.objects.filter(
                member_id=user_id,
                team_id=team_id
            ).values_list("role_id", flat=True)
            roles = [
                {
                    "value": x['id'],
                    "label": x['name']
                } for x in Role.objects.filter(id__in=multiple_roles).exclude(id__in=assign_roles).values("id", "name")
            ]
        else:
            roles = [{
                "value": self.request.user.roles.id,
                "label": self.request.user.roles.name
            }]
        data = {"roles": roles}
        return Response(data)

    def post(self, request):
        role_id = request.data.get("role_id")
        status_code = status.HTTP_200_OK
        if role_id in request.user.multiple_roles or self.request.user.roles_id == role_id:
            if role_id == str(self.request.user.roles_id):
                data = {"detail": "Role already assign"}
            else:
                # Will generate new token
                user = User.objects.filter(id=request.user.id)
                user.update(roles_id=role_id)
                token = self.generate_token(user.first())
                data = {"token": token}
        else:
            data = {"detail": "Role doesn't exist"}
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(data, status=status_code)

    def generate_token(self, user):
        iat = datetime.datetime.utcnow()
        try:
            permissions = list(user.roles.permissions.values_list('codename', flat=True))
        except:
            permissions = None
        roles = Role.objects.filter(id__in=user.multiple_roles)
        token = {
            "token_type": "access",
            "jti": str(uuid.uuid4()),
            "iat": iat,
            "exp": iat + SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            "user_id": str(user.id),
            "permissions": permissions,
            "role": user.roles.name if user.roles else None,
            "role_id": str(user.roles.id) if user.roles else None,
            "roles": [{"id": str(x.id), "name": x.name} for x in roles] if roles else None,
            'username': user.username,
            "email": user.email,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
            "company": str(user.profile.company.id) if user.profile else None,
            "profile_image": str(user.profile.file_url) if user.profile else None
        }
        return jwt.encode(token, SIMPLE_JWT['SIGNING_KEY'], algorithm=SIMPLE_JWT['ALGORITHM'])


# for x in User.objects.all().exclude(multiple_roles__isnull=False):
#     if x.roles is not None:
#         x.multiple_roles = [str(x.roles.id)]
#         x.save()
# print("Terminated")
