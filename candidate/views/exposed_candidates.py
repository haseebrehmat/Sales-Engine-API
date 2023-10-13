from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from authentication.models.company import Company
from candidate.models.exposed_candidates import ExposedCandidate
from candidate.serializers.exposed_candidate import ExposedCandidateSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class ExposedCandidateListAPIView(APIView):
    serializer_class = ExposedCandidateSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = ExposedCandidate.objects.filter(candidate__company_id=request.user.profile.company.id)\
            .distinct("candidate_id")
        data = []

        if len(queryset) > 0:
            search = self.request.GET.get("search", "")
            if search != "":
                queryset = queryset.filter(candidate__name__icontains=search)
                serializer = ExposedCandidateSerializer(queryset, many=True)
            else:
                serializer = ExposedCandidateSerializer(queryset, many=True)
            data = {"candidates": serializer.data}
            queryset = Company.objects.filter(status=True).exclude(id=request.user.profile.company.id)
            companies = [{"id": x.id, "name": x.name} for x in queryset]
            data['companies'] = companies
        return Response(data)

    def post(self, request):
        company_ids = request.data.get("company_ids", [])
        candidate_ids = request.data.get("candidate_ids", [])
        if company_ids == [] or candidate_ids == []:
            message = "Candidate or Company should not be empty"
            status_code = status.HTTP_406_NOT_ACCEPTABLE
            return Response({"detail": message}, status_code)
        data = []
        for candidate_id in candidate_ids:
            for company_id in company_ids:
                data.append(
                    {
                        "company_id": company_id,
                        "candidate_id": candidate_id,
                        "company": company_id,
                        "candidate": candidate_id,
                    }
                )

        serializer = ExposedCandidateSerializer(data=data, many=True)
        if serializer.is_valid():
            message, status_code = self.save_exposed_candidate(request, data, serializer)
            return Response({"detail": message}, status_code)

        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    @transaction.atomic
    def save_exposed_candidate(self, request, data, serializer):
        try:
            for x in data:
                ExposedCandidate.objects.filter(candidate_id=x["candidate_id"],
                                                candidate__company=request.user.profile.company).delete()
            serializer.create(serializer.validated_data)
            message = "Candidate Exposed successfully"
            status_code = status.HTTP_201_CREATED
        except Exception as e:
            status_code = status.HTTP_406_NOT_ACCEPTABLE
            if "unique constraint" in str(e):
                message = "Candidate already exposed"
            else:
                message = str(e)
        return message, status_code


class CandidateExposedDetailView(APIView):
    # serializer_class = ExposedCandidateSerializer
    # pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        queryset = ExposedCandidate.objects.filter(pk=pk, candidate__company_id=request.user.profile.company.id).first()
        data = []
        if queryset is not None:
            serializer = ExposedCandidateSerializer(queryset, many=False)
            data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    # def put(self, request, pk):
    #     company_ids = request.data.get("company_ids", [])
    #     candidate_ids = request.data.get("candidate_ids", [])
    #     if company_ids == [] or candidate_ids == []:
    #         message = "Candidate or Company should not be empty"
    #         status_code = status.HTTP_406_NOT_ACCEPTABLE
    #         return Response({"detail": message}, status_code)
    #     data = []
    #     for candidate_id in candidate_ids:
    #         for company_id in company_ids:
    #             data.append(
    #                 {
    #                     "company_id": company_id,
    #                     "candidate_id": candidate_id,
    #                     "allowed_status": request.data.get("allowed_status", False)
    #                 }
    #             )
    #
    #     queryset = ExposedCandidate.objects.filter(pk=pk,
    #                                                candidate__company_id=self.request.user.profile.company.id).first()
    #     serializer = ExposedCandidateSerializer(instance=queryset, data=data)
    #     if serializer.is_valid():
    #         try:
    #             serializer.save(candidate_id=request.data.get("candidate_id"),
    #                             company_id=request.data.get("company_id"))
    #             message = "Exposed Candidate updated successfully"
    #             status_code = status.HTTP_201_CREATED
    #             return Response({"detail": message}, status_code)
    #         except Exception as e:
    #             return Response({"detail": "Candidate already exposed"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    #     data = serializer_errors(serializer)
    #     raise InvalidUserException(data)

    def delete(self, request, pk):
        try:
            company = request.user.profile.company
            queryset = ExposedCandidate.objects.filter(pk=pk, candidate__company=company)
            candidate = queryset.first().candidate
            if ExposedCandidate.objects.filter(candidate=candidate, candidate__company=company).count() == 1:
                queryset.delete()
                ExposedCandidate.objects.create(candidate=candidate)
            else:
                queryset.delete()

            return Response({"detail": "Candidate Unexposed successfully"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "You dont have permission to unexposed this candidate"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)


class PoolCandidateListAPIView(ListAPIView):
    serializer_class = ExposedCandidateSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = ExposedCandidate.objects.filter(company_id=self.request.user.profile.company.id)
        # queryset = ExposedCandidate.objects.filter(candidate__company_id=self.request.user.profile.company.id)
        return queryset


class PoolCandidateDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        queryset = ExposedCandidate.objects.filter(pk=pk, company_id=self.request.user.profile.company.id).first()
        data = []
        if queryset is not None:
            serializer = ExposedCandidateSerializer(queryset, many=False)
            data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
