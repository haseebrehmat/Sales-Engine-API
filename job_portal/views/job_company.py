from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from job_portal.models import JobDetail, JobArchive, BlockJobCompany
from job_portal.paginations.job_company import JobCompanyPagination
from job_portal.serializers.job_company import JobCompanySerializer


class JobCompaniesList(ListAPIView):
    serializer_class = JobCompanySerializer
    pagination_class = JobCompanyPagination
    queryset = None

    def get_queryset(self):
        search = self.request.query_params['search']
        search_query = Q()
        if search:
            search = search.lower()
            search_query = Q(company_name__icontains=search)
        block_job_companies = [company.lower() for company in list(
            BlockJobCompany.objects.filter(company=self.request.user.profile.company).filter(search_query).values_list(
                'company_name',
                flat=True))]
        companies = list(JobDetail.objects.filter(search_query).values_list('company_name', flat=True))
        companies.extend(list(JobArchive.objects.filter(search_query).values_list('company_name', flat=True)))
        all_companies = [{"company": company, "is_block": True} for company in block_job_companies]
        all_companies.extend([{"company": company, "is_block": False} for company in list(
            set(company.lower() for company in companies if
                company.lower() and company.lower() not in block_job_companies))])
        self.queryset = all_companies
        return all_companies

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data, self.queryset)

    def post(self, request):
        try:
            user_company = self.request.user.profile.company
            company_name = request.data.get("company_name").lower()
            obj = BlockJobCompany.objects.filter(company=user_company, company_name=company_name).first()
            is_block = request.data.get("is_block")
            if user_company is None or company_name is None or is_block is None:
                return Response({"detail": "Invalid input, something is missing."},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            if obj:
                if not is_block:
                    msg = 'This job company is deleted from block list!'
                    status_code = status.HTTP_200_OK
                    obj.delete()
                else:
                    msg = 'This job company is already marked as blocked!'
                    status_code = status.HTTP_406_NOT_ACCEPTABLE
            else:
                if is_block:
                    BlockJobCompany.objects.create(company=user_company, company_name=company_name)
                    msg = 'Job company blocked successfully!'
                    status_code = status.HTTP_200_OK
                else:
                    msg = 'Job company is not blocked!'
                    status_code = status.HTTP_406_NOT_ACCEPTABLE
            return Response({'detail': msg}, status=status_code)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
