from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from job_portal.models import JobDetail, JobArchive, BlockJobCompany
from job_portal.paginations.job_company import JobCompanyPagination
from job_portal.serializers.job_company import JobCompanySerializer


class JobCompaniesList(ListAPIView):
    serializer_class = JobCompanySerializer
    pagination_class = JobCompanyPagination

    def get_queryset(self):
        block_job_companies = list(
            BlockJobCompany.objects.filter(company=self.request.user.profile.company).values_list('company_name',
                                                                                                  flat=True))
        companies = list(JobDetail.objects.values_list('company_name', flat=True))
        companies.extend(list(JobArchive.objects.values_list('company_name', flat=True)))
        all_companies = [{"company": company, "is_block": True} for company in block_job_companies]
        all_companies.extend([{"company": company, "is_block": False} for company in list(
            set(company for company in companies if company and company not in block_job_companies))])
        return all_companies

    def post(self, request):
        user_company = self.request.user.profile.company
        company_name = request.data.get("company_name", "").lower()
        obj = BlockJobCompany.objects.filter(company=user_company, company_name=company_name).first()
        is_block = request.data.get("is_block")
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
