from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from candidate.models import CandidateProjects, Candidate
from candidate.serializers.candidate_projects import CandidateProjectSerializer
from settings.utils.helpers import serializer_errors
class CandidateProjectDetailView(APIView):

    def get(self, request, pk):
        print(pk)
        queryset = CandidateProjects.objects.filter(candidate_id=pk)
        if queryset is not None:
            serializer = CandidateProjectSerializer(queryset, many=True)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
    def put(self, request, pk):
        queryset = Candidate.objects.filter(pk=pk).first()
        data = request.data
        serializer = CandidateProjectSerializer(instance=queryset, data=data)
        if serializer.is_valid():
            projects = request.data.get("projects", "")
            serializer.save(candidate=queryset, projects=projects)
            message = "Candidate Projects Updated successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)