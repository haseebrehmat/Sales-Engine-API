from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from job_portal.models import BlacklistJobs, JobDetail


class BlackListJobsView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # add word to blacklist and mark all companies blacklisted
        if request.user.profile and request.user.profile.company:
            company_name = request.data.get('company_name', False)
            if company_name:
                company_name = company_name.lower()
                black_company, is_created = BlacklistJobs.objects.get_or_create(company=request.user.profile.company,
                                                                                company_name=company_name)

                JobDetail.objects.filter(company_name__iexact=company_name).update(block=True)
                return Response({"detail": "User company has been blacklisted"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Company name field is empty"},
                                status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User has no company assign"}, status=status.HTTP_200_OK)


class NonBlackListJobsView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # add word to blacklist and mark all companies blacklisted
        if request.user.profile and request.user.profile.company:
            company_name = request.data.get('company_name',None)
            if company_name:
                BlacklistJobs.objects.filter(company=request.user.profile.company,company_name__iexact=company_name).delete()
                JobDetail.objects.filter(company_name__iexact=company_name).update(block=False)
                return Response({"detail": "User company has been removed from blacklisted"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Company name field is empty"},
                                status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User has no company assign"}, status=status.HTTP_200_OK)


class JobSourcesView(APIView):
    def get(self, request):
        jobs = list(set(JobDetail.objects.all().values_list("company_name", flat=True)))
        return Response({"job_sources": [job for job in jobs if len(job) > 0]})
