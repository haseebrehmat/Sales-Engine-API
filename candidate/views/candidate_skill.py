from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from candidate.models import CandidateSkills, Skills
from candidate.serializers.skills import CandidateSkillsSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class CandidateSkillsListView(ListAPIView):
    serializer_class = CandidateSkillsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = CandidateSkills.objects.all()
        return queryset

    def post(self, request):
        serializer = CandidateSkillsSerializer(data=request.data, many=False)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Skills.objects
            serializer.create(data)

            message = "CandidateSkills created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)


class CandidateSkillsDetailView(APIView):

    def get(self, request, pk):
        queryset = CandidateSkills.objects.filter(pk=pk).first()
        data = []
        if queryset is not None:
            serializer = CandidateSkillsSerializer(queryset, many=False)
            data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = CandidateSkills.objects.filter(pk=pk).first()
        serializer = CandidateSkillsSerializer(instance=queryset, data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=request.user.profile.company.id)
            message = "CandidateSkills updated successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        CandidateSkills.objects.filter(pk=pk).delete()
        return Response({"detail": "CandidateSkills deleted successfully"}, status.HTTP_200_OK)





