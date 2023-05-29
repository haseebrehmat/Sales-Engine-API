from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from candidate.models.exposed_candidates import ExposedCandidate
from candidate.serializers.exposed_candidate import ExposedCandidateSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class ExposedCandidateListAPIView(ListAPIView):
    serializer_class = ExposedCandidateSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        #queryset = ExposedCandidate.objects.filter(company_id=self.request.user.profile.company.id)
        queryset = ExposedCandidate.objects.filter(candidate__company_id=self.request.user.profile.company.id)
        return queryset

    def post(self, request):
        serializer = ExposedCandidateSerializer(data=request.data, many=False)
        if serializer.is_valid():
            try:
                serializer.validated_data["candidate_id"] = request.data.get("candidate_id")
                serializer.validated_data["company_id"] = request.data.get("company_id")
                
                serializer.create(serializer.validated_data)
                message = "Candidate Exposed successfully"
                status_code = status.HTTP_201_CREATED
                return Response({"detail": message}, status_code)
            except Exception as e:
                return Response({"detail": "Candidate already exposed"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

class CandidateExposedDetailView(APIView):
    # serializer_class = ExposedCandidateSerializer
    # pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk):
        queryset = ExposedCandidate.objects.filter(pk=pk,candidate__company_id=self.request.user.profile.company.id).first()
        data = []
        if queryset is not None:
            serializer = ExposedCandidateSerializer(queryset, many=False)
            data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = ExposedCandidate.objects.filter(pk=pk,candidate__company_id=self.request.user.profile.company.id ).first()
        serializer = ExposedCandidateSerializer(instance=queryset, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(candidate_id=request.data.get("candidate_id"),company_id=request.data.get("company_id"))
                message = "Exposed Candidate updated successfully"
                status_code = status.HTTP_201_CREATED
                return Response({"detail": message}, status_code)
            except Exception as e:
                return Response({"detail": "Candidate already exposed"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        try:
            ExposedCandidate.objects.filter(pk=pk,candidate__company_id=self.request.user.profile.company.id).delete()
            return Response({"detail": "Candidate Unexposed successfully"}, status.HTTP_200_OK)
        except Exception as e:
                return Response({"detail": "You dnt have permission to unexposed this candidate"}, status=status.HTTP_406_NOT_ACCEPTABLE)



class PoolCandidateListAPIView(ListAPIView):
    serializer_class = ExposedCandidateSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = ExposedCandidate.objects.filter(company_id=self.request.user.profile.company.id)
        #queryset = ExposedCandidate.objects.filter(candidate__company_id=self.request.user.profile.company.id)
        return queryset
class PoolCandidateDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk):
        queryset = ExposedCandidate.objects.filter(pk=pk,company_id=self.request.user.profile.company.id).first()
        data = []
        if queryset is not None:
            serializer = ExposedCandidateSerializer(queryset, many=False)
            data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
