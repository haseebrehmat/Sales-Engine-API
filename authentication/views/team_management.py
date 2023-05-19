from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from authentication.models.team_management import Team
from authentication.permissions import TeamPermissions
from authentication.serializers.team_management import TeamManagementSerializer
from settings.utils.helpers import serializer_errors


class TeamView(ListAPIView):
    permission_classes = (TeamPermissions, )
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'reporting_to__username', 'reporting_to__email', 'members__username',  'members__email']

    def get(self, request):
        print()
        queryset = Team.objects.filter(reporting_to__profile__company=request.user.profile.company).select_related()
        queryset = self.filter_queryset(queryset)
        serializer = TeamManagementSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TeamManagementSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            data["reporting_to"] = request.data.get("reporting_to")
            data["members"] = request.data.get("members")
            serializer.create(data)

            message = "Team created successfully!"
            status_code = status.HTTP_201_CREATED
            return Response({'detail': message}, status=status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)


class TeamDetailView(APIView):
    permission_classes = (TeamPermissions, )

    def get(self, request, pk):
        queryset = Team.objects.filter(pk=pk).first()
        serializer = TeamManagementSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Team.objects.filter(pk=pk).first()
        serializer = TeamManagementSerializer(queryset, request.data)

        if serializer.is_valid():
            serializer.save(reporting_to=request.data.get("reporting_to"), members=request.data.get("members"))

            message = "Team updated successfully!"
            status_code = status.HTTP_200_OK
            return Response({'detail': message}, status=status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        Team.objects.filter(pk=pk).delete()
        return Response({'detail': "Team deleted successfully"}, status=status.HTTP_200_OK)