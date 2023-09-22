from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from job_portal.models import JobDetail


@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_tech_keywords(request):
    keywords = JobDetail.objects.all().values_list("tech_stacks", flat=True)
    data = []
    for x in keywords:
        data.extend(x)
    return Response({"keywords": list(set(data))})
