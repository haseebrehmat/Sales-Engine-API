from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from job_portal.models import JobDetail, JobArchive, TechStats


@api_view(['GET'])
# @permission_classes((AllowAny, ))
def get_tech_keywords(request):
    keywords_from_detail = (JobDetail.objects.exclude(Q(tech_stacks=None) | Q(tech_stacks=[]))
                            .values_list("tech_stacks", flat=True))
    keywords_from_archive = (
        JobArchive.objects.exclude(Q(tech_keywords=None) | Q(tech_keywords='') | Q(tech_keywords__contains="['']"))
        .values_list("tech_keywords", flat=True))
    keywords_from_stats = TechStats.objects.exclude(Q(name=None) | Q(name='')).values_list("name", flat=True)
    keywords = [x.split(",") for x in keywords_from_archive if x]
    keywords.extend(list(keywords_from_detail))
    data = []
    for x in keywords:
        data.extend(x)
    data.extend(list(keywords_from_stats))
    return Response({"keywords": list(set(data))})
