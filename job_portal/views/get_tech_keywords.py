from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from job_portal.models import JobDetail, JobArchive, TechStats


@api_view(['GET'])
#@permission_classes((AllowAny, ))
def get_tech_keywords(request):
    keywords_from_detail = JobDetail.objects.exclude(tech_stacks=None).values_list("tech_stacks", flat=True)
    keywords_from_archive = JobArchive.objects.exclude(tech_keywords=None).values_list("tech_keywords", flat=True)
    keywords_from_stats = TechStats.objects.exclude(name=None).values_list("name", flat=True)
    keywords = [x.split(",") for x in keywords_from_archive]
    keywords.extend(list(keywords_from_detail))
    data = []
    for x in keywords:
        data.extend(x)
    data.extend(list(keywords_from_stats))
    return Response({"keywords": list(set(data))})