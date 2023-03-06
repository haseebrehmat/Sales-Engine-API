from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from authentication.models import Profile
from authentication.serializers.profile import ProfileSerializer
from settings.utils.helpers import serializer_errors


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Profile.objects.filter(user_id=request.user.id).first()
        serializer = ProfileSerializer(queryset, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request):
        instance = Profile.objects.filter(user_id=request.user.id).first()
        data = request.data
        data["user_id"] = request.user.id
        if instance is None:
            print(instance)
            instance = Profile.objects.create(user_id=request.user.id)
        serializer = ProfileSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=data.get("company"))
            return Response({"detail": "Profile updated successfully"}, status=status.HTTP_200_OK)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

