from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from pseudos.models.configurations import VerticalConfigurations
from pseudos.serializers.configurations import ConfigurationSerializer
from settings.utils.helpers import serializer_errors


class ConfigurationView(APIView):
    permission_classes = (AllowAny,)
    serializer = ConfigurationSerializer

    def get(self, request):
        qs = VerticalConfigurations.objects.filter(user=request.user)
        data = []
        if qs.exists():
            serializer = self.serializer(qs.first(), many=False)
            data = serializer.data
        return Response(data, status.HTTP_200_OK)

    def post(self, request):

        data = request.data
        serializer = self.serializer(data=data, many=False)
        if not serializer.is_valid():
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

        data["user_id"] = request.user.id

        qs = VerticalConfigurations.objects.filter(user=request.user)
        if qs.exists():
            qs.update(**data)
        else:
            VerticalConfigurations.objects.create(**data)

        return Response({"detail": "Configurations saved"}, status=status.HTTP_200_OK)



