from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from authentication.models import Profile, User
from authentication.serializers.profile import ProfileSerializer
from settings.utils.helpers import serializer_errors


class ProfileView(APIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = Profile.objects.filter(user_id=request.user.id).first()
        serializer = ProfileSerializer(queryset, many=False)
        data = []
        if len(serializer.data) > 0:
            data = serializer.data
            data.update(**data["user"])
            try:
                data['role'] = request.user.roles.name
            except:
                data['role'] = ""
            del data["user"]

        return Response(data, status.HTTP_200_OK)

    def put(self, request):
        conditions = [
            request.data.get("first_name", "") != "",
            request.data.get("last_name", "") != "",
            request.data.get("email", "") != "",
            request.data.get("username", "") != "",
        ]
        username = request.data.get("username", request.user.username)
        email = request.data.get("email", request.user.email)
        if not all(conditions):
            return Response({"detail": "Fields cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if request.user.email != email:
            if User.objects.filter(email__iexact=email).count() > 0:
                return Response({"detail": "User with this email already exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        instance = Profile.objects.filter(user_id=request.user.id).first()
        data = request.data.copy()
        data["user_id"] = request.user.id
        if instance is None:    # Incase Profile Doesn't exist
            instance = Profile.objects.create(user_id=request.user.id)
        serializer = ProfileSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(username=username, email=email)
            return Response({"detail": "Profile updated successfully"}, status=status.HTTP_200_OK)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)
