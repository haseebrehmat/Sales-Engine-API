import datetime
import uuid
import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import Role, User, TeamRoleVerticalAssignment, MultipleRoles
from settings.base import SIMPLE_JWT


class MultipleRoleManagement(APIView):

    def get(self, request):
        multiple_roles = []
        user_id = request.GET.get("user_id")
        team_id = request.GET.get("team_id")
        if user_id:
            qs = User.objects.filter(id=user_id).first()
            if qs:
                multiple_roles = MultipleRoles.objects.filter(user=qs)
        else:
            multiple_roles = MultipleRoles.objects.filter(user=request.user)
        if multiple_roles:
            # exclude team based assign roles from the view
            assign_roles = TeamRoleVerticalAssignment.objects.filter(
                member_id=user_id,
                team_id=team_id
            ).values_list("role_id", flat=True)
            roles = [
                {
                    "value": x['role_id'],
                    "label": x['role__name']
                } for x in multiple_roles.exclude(role_id__in=assign_roles).values("role_id", "role__name")
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
        conditions = [
            MultipleRoles.objects.filter(user=request.user, role_id=role_id).exists(),
            self.request.user.roles_id == role_id
        ]
        if any(conditions):
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
        roles = MultipleRoles.objects.filter(user=user)
        token = {
            "token_type": "access",
            "jti": str(uuid.uuid4()),
            "iat": iat,
            "exp": iat + SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            "user_id": str(user.id),
            "permissions": permissions,
            "role": user.roles.name if user.roles else None,
            "role_id": str(user.roles.id) if user.roles else None,
            "roles": [{"id": str(x.role.id), "name": x.role.name} for x in roles] if roles else None,
            'username': user.username,
            "email": user.email,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
            "company": str(user.profile.company.id) if user.profile else None,
            "profile_image": str(user.profile.file_url) if user.profile else None
        }
        return jwt.encode(token, SIMPLE_JWT['SIGNING_KEY'], algorithm=SIMPLE_JWT['ALGORITHM'])
#
# print("Started")
# bulk_instances = [MultipleRoles(user=x, role=x.roles) for x in User.objects.all() if x.roles is not None]
# MultipleRoles.objects.bulk_create(bulk_instances, batch_size=500, ignore_conflicts=True)
# print("Terminated")

