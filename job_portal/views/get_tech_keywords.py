from rest_framework.decorators import api_view
from rest_framework.response import Response

from job_portal.models import JobDetail


@api_view(['GET'])
def get_tech_keywords(request):
    keywords = set(JobDetail.objects.all().values_list("tech_keywords", flat=True))
    return Response({"keywords": keywords})
