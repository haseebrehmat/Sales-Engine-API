from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from candidate.models import Candidate, Skills, ExposedCandidate
from candidate.serializers.candidate import CandidateSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class CandidateListView(ListAPIView):
    serializer_class = CandidateSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        company = self.request.user.profile.company
        queryset = Candidate.objects.filter(
            company=company)
        candidates = ExposedCandidate.objects.filter(company=company).values_list("candidate_id", flat=True)

        queryset |= Candidate.objects.filter(id__in=candidates)

        return queryset

    def post(self, request):
        serializer = CandidateSerializer(data=request.data, many=False)
        if serializer.is_valid():
            data = serializer.validated_data
            data["company_id"] = request.user.profile.company.id
            data["designation_id"] = request.data.get("designation")
            skills = request.data.get("skills")
            data['skills'] = skills
            data['password'] = request.data.get("password", "User@123")
            data['email'] = request.data.get("email", "")
            serializer.create(data)
            message = "Candidate created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)


class CandidateDetailView(APIView):

    def get(self, request, pk):
        queryset = Candidate.objects.filter(pk=pk).first()
        data = []
        if queryset is not None:
            serializer = CandidateSerializer(queryset, many=False)
            data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Candidate.objects.filter(pk=pk).first()
        serializer = CandidateSerializer(instance=queryset, data=request.data)
        if serializer.is_valid():
            skills = request.data.get("skills")
            serializer.save(company_id=request.user.profile.company.id, skills=skills)
            message = "Candidate updated successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        Candidate.objects.filter(pk=pk).delete()
        return Response({"detail": "Candidate deleted successfully"}, status.HTTP_200_OK)
