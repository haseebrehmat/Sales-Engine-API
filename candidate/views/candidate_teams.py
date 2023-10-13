from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from authentication.models.company import Company
from candidate.models import CandidateTeam, ExposedCandidate
from candidate.serializers.candidate_teams import CandidateTeamsSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class CandidateTeamsListView(APIView):
    serializer_class = CandidateTeamsSerializer
    pagination_class = CustomPagination

    def get(self, request):
        # Teams belongs to users Company
        queryset = CandidateTeam.objects.filter(company=self.request.user.profile.company_id)
        search = self.request.GET.get("search", "")
        if search != "":
            queryset = queryset.filter(name__icontains=search)
        data = {}
        serializer = CandidateTeamsSerializer(queryset, many=True)
        data["teams"] = serializer.data
        queryset = ExposedCandidate.objects.filter(candidate__company_id=request.user.profile.company_id).distinct('candidate_id')
        exposed_candidates = [{"id": x.id, "name": x.candidate.name,
                               "allowed_status": x.allowed_status} for x in queryset]
        data['exposed_candidates'] = exposed_candidates
        queryset = Company.objects.filter(status=True).exclude(id=request.user.profile.company.id)
        companies = [{"id": x.id, "name": x.name} for x in queryset]
        data['companies'] = companies
        return Response(data)

    def post(self, request):
        serializer = CandidateTeamsSerializer(data=request.data, many=False)
        conditions = [
            request.data.get("name", "") != ""
        ]
        if all(conditions):
            if serializer.is_valid():
                data = serializer.validated_data
                data["company_id"] = request.user.profile.company.id
                exposed_candidates = request.data.get("exposed_candidates", "")
                data['exposed_candidates'] = exposed_candidates
                serializer.create(data)
                message = "Candidate Team created successfully"
                status_code = status.HTTP_201_CREATED
                return Response({"detail": message}, status_code)
            data = serializer_errors(serializer)
            if data == "non_field_errors: The fields company, name must make a unique set.":
                data = "Team Already Exist"
            raise InvalidUserException(data)
        else:
            message = "Fields Cannot be empty"
            status_code = status.HTTP_406_NOT_ACCEPTABLE
            return Response({"detail": message}, status_code)


class CandidateTeamsDetailView(APIView):

    def get(self, request, pk):
        queryset = CandidateTeam.objects.filter(pk=pk).first()
        data = []
        if queryset is not None and queryset.company.id == request.user.profile.company_id:
            serializer = CandidateTeamsSerializer(queryset, many=False)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            message = "Team not found"
            status_code = status.HTTP_404_NOT_FOUND
            return Response({"detail": message}, status_code)

    def put(self, request, pk):
        queryset = CandidateTeam.objects.filter(pk=pk).first()
        data = request.data
        data["company_id"] = request.user.profile.company.id
        serializer = CandidateTeamsSerializer(instance=queryset, data=data)
        conditions = [
            request.data.get("name", "") != ""
        ]
        if all(conditions):
            if serializer.is_valid():
                exposed_candidates = request.data.get("exposed_candidates", "")
                serializer.save(exposed_candidates=exposed_candidates)
                message = "Candidate Team updated successfully"
                status_code = status.HTTP_201_CREATED
                return Response({"detail": message}, status_code)
            data = serializer_errors(serializer)
            raise InvalidUserException(data)
        else:
            message = "Fields Cannot be empty"
            status_code = status.HTTP_406_NOT_ACCEPTABLE
            return Response({"detail": message}, status_code)

    def delete(self, request, pk):
        CandidateTeam.objects.filter(pk=pk).delete()
        return Response({"detail": "Candidate Team deleted successfully"}, status.HTTP_200_OK)





