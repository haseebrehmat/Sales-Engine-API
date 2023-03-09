from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from job_portal.models import BlacklistJobs, JobDetail
from job_portal.serializers.black_list import BlacklistSerializer


# class BlackListJobsView(APIView):
#     permission_classes = (IsAuthenticated, )
#
#     def get(self, request):
#         if request.user.profile and request.user.profile.company:
#             queryset = BlacklistJobs.objects.filter(company_id=request.user.profile.company)
#             serializer = BlacklistSerializer(queryset, many=True)
#             data = serializer.data
#             return Response(data, status=status.HTTP_200_OK)
#         return Response({"detail": "No profile or company assign to user"}, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         # add word to blacklist and mark all companies blacklisted
#         check = BlacklistJobs.objects.filter(company_id=request.data.get("company")).update(**request.data)
#         if check == 0:
#             company_id = request.data.pop("company")
#             check = BlacklistJobs.objects.create(**request.data, company_id=company_id)
#         if check != 0:
#             return Response({"detail": "Settings saved successfully"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"detail": "Error in saving settings"}, status=status.HTTP_200_OK)
#
#     def delete(self, request,id):
#         queryset = BlacklistJobs.objects.filter(id=id,company_id=request.user.profile.company.id).delete()
#         return Response({"detail": "Company removed successfully"}, status=status.HTTP_200_OK)


class BlackListJobsView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # add word to blacklist and mark all companies blacklisted
        company = request.user.profile.company
        company_name = request.data.get('company_name',None)
        if company and company_name:
            black_company,is_created = BlacklistJobs.objects.get_or_create(company=request.user.profile.company,company_name=company_name)
            JobDetail.objects.filter(company_name__iexact=company_name).update(block=True)
            return Response({"detail": "User company has been blacklisted"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User has no company assign or company_name field is empty"}, status=status.HTTP_200_OK)

class NonBlackListJobsView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        # add word to blacklist and mark all companies blacklisted
        company = request.user.profile.company
        company_name = request.data.get('company_name',None)
        if company and company_name:
            BlacklistJobs.objects.filter(company=request.user.profile.company,company_name=company_name).delete()
            JobDetail.objects.filter(company_name__iexact=company_name).update(block=False)
            return Response({"detail": "User company has been removed from blacklisted"},
                            status=status.HTTP_200_OK)

        else:
            return Response({"detail": "User has no company assign or company_name field is empty"}, status=status.HTTP_200_OK)



class JobSourcesView(APIView):
    def get(self, request):
        jobs = list(set(JobDetail.objects.all().values_list("company_name", flat=True)))
        return Response({"job_sources": [job for job in jobs if len(job) > 0]})
