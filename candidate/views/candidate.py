from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from authentication.exceptions import InvalidUserException
from authentication.models import User, Profile
from candidate.models import Candidate, Skills, ExposedCandidate, SelectedCandidate, Regions
from candidate.serializers.candidate import CandidateSerializer
from candidate.pagination.custom_pagination import CustomPagination
from lead_management.models import Lead
from settings.utils.helpers import serializer_errors


class CandidateListView(ListAPIView):
    serializer_class = CandidateSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        name_query = Q()
        phone_query = Q()
        email_query = Q()
        data = dict()
        company = self.request.user.profile.company
        queryset = Candidate.objects.filter(
            company=company)
        search = self.request.GET.get("search", "")
        if search != "":
            name_query = Q(name__icontains=search)
            phone_query = Q(phone__icontains=search)
            email_query = Q(email__icontains=search)
            queryset = queryset.filter(name_query | phone_query | email_query)
        else:
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
        if request.data.get('candidate', False) and request.data.get('login_status') != None:
            cand = Candidate.objects.filter(pk=request.data.get('candidate')).first()
            email = cand.email
            qs = User.objects.filter(email=email).first()
            if qs:
                Profile.objects.filter(user=qs).update(is_restricted=request.data.get('login_status'))
                return Response({"detail": "Candidate updated successfully"})
            else:
                return Response({"detail": "Candidate not found"})

        serializer = CandidateSerializer(data=request.data, many=False)
        if serializer.is_valid():
            data = serializer.validated_data
            data["company_id"] = request.user.profile.company.id
            designation = request.data.get("designation", "")
            data["designation_id"] = designation.get("value", "")
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
            designation = request.data.get("designation", "")
            serializer.save(company_id=request.user.profile.company.id,
                            skills=skills, tools=tools, regions=regions,
                            designation_id=designation.get("value", ""))
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
        else:
            message = "Your Profile has been deleted by company owner"
            status_code = status.HTTP_404_NOT_FOUND
            return Response({"detail": message}, status_code)
