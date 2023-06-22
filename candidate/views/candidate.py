from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from candidate.models import Candidate, Skills, ExposedCandidate, SelectedCandidate, Regions
from candidate.serializers.candidate import CandidateSerializer
from candidate.pagination.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class CandidateListView(ListAPIView):
    serializer_class = CandidateSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        data = dict()
        company = self.request.user.profile.company
        queryset = Candidate.objects.filter(
            company=company)
        candidates = ExposedCandidate.objects.filter(company=company).values_list("candidate_id", flat=True)
        queryset |= Candidate.objects.filter(id__in=candidates)
        return queryset

    def post(self, request):
        if request.data.get('candidate', False) and request.data.get('status') != None:
            qs = SelectedCandidate.objects.filter(
                company=request.user.profile.company,
                candidate_id=request.data.get('candidate', False))

            if qs.exists():
                SelectedCandidate.objects.filter(
                company=request.user.profile.company,
                candidate_id=request.data.get('candidate')).update(status=request.data.get('status', False))
            else:
                SelectedCandidate.objects.create(
                company=request.user.profile.company,
                candidate_id=request.data.get('candidate'),
                status = request.data.get('status', False)
                )
            return Response({"detail": "Candidate updated successfully"})

        serializer = CandidateSerializer(data=request.data, many=False)
        if serializer.is_valid():
            data = serializer.validated_data
            data["company_id"] = request.user.profile.company.id
            data["designation_id"] = request.data.get("designation", "")
            skills = request.data.get("skills", "")
            data['skills'] = skills
            regions = request.data.get("regions", "")
            data['regions'] = regions
            tools = request.data.get("tools", "")
            data['tools'] = tools
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
        data = dict()
        if queryset is not None:
            serializer = CandidateSerializer(queryset, many=False)
            data["candidate"] = serializer.data
            data["all_regions"] = [{"id": x.id, "name": x.region} for x in Regions.objects.all()]
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Candidate.objects.filter(pk=pk).first()
        data = request.data
        serializer = CandidateSerializer(instance=queryset, data=data)
        if serializer.is_valid():
            skills = request.data.get("skills", "")
            tools = request.data.get("tools", "")
            regions = request.data.get("regions", "")
            serializer.save(company_id=request.user.profile.company.id,
                            skills=skills, tools=tools, regions=regions,
                            designation_id=request.data.get("designation", queryset.designation_id))
            message = "Candidate updated successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        Candidate.objects.filter(pk=pk).delete()
        return Response({"detail": "Candidate deleted successfully"}, status.HTTP_200_OK)


class CandidateProfileDetailView(APIView):

    def get(self, request):
        queryset = Candidate.objects.filter(company_id=request.user.profile.company.id, email__iexact=request.user.email).first()
        data = dict()
        if queryset is not None:
            serializer = CandidateSerializer(queryset, many=False)
            data["candidate"] = serializer.data
            data["all_regions"] = [{"id": x.id, "name": x.region} for x in Regions.objects.all()]
        return Response(data, status=status.HTTP_200_OK)