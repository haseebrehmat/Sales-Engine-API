from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from job_portal.models import TrendsAnalytics
from job_portal.paginations.trend_analytics import TrendAnalyticsPagination
from job_portal.serializers.trends_analytics import TrendsAnalyticsSerializer
from settings.utils.helpers import serializer_errors
from utils.helpers import saveLogs
from rest_framework.response import Response
from rest_framework import status


class TrendsAnalyticsListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TrendsAnalyticsSerializer
    pagination_class = TrendAnalyticsPagination
    filter_backends = [SearchFilter]
    search_fields = ['category']

    def get_queryset(self):
        queryset = TrendsAnalytics.objects.all()
        return queryset

    def post(self, request):
        serializer = TrendsAnalyticsSerializer(data=request.data, many=False)
        category = request.data.get('category', '').lower()
        tech_stacks = request.data.get('tech_stacks', '').lower()
        obj = TrendsAnalytics.objects.filter(category__iexact=category)
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        if obj:
            msg = 'Failure! This category is already created.'
        elif serializer.is_valid():
            if not tech_stacks:
                msg = 'Failure! Tech stacks field should not be empty.'
            else:
                TrendsAnalytics.objects.create(category=category, tech_stacks=tech_stacks)
                msg = 'New category created for trends analytics.'
                status_code = status.HTTP_201_CREATED
        else:
            msg = serializer_errors(serializer)
        return Response({"detail": msg}, status=status_code)


class TrendsAnalyticsDetailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            obj = TrendsAnalytics.objects.get(id=pk)
            serializer = TrendsAnalyticsSerializer(obj, many=False)
            return Response(serializer.data)
        except Exception as e:
            saveLogs(e)
            return Response({"detail": "Invalid Trend Analytics id"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, pk):
        try:
            obj = TrendsAnalytics.objects.get(id=pk)
            category = request.data.get('category', '')
            tech_stacks = request.data.get('tech_stacks', '')
            status_code = status.HTTP_406_NOT_ACCEPTABLE
            trend_analytics = TrendsAnalytics.objects.filter(category__iexact=category).first()
            if trend_analytics and trend_analytics.id != obj.id:
                msg = f'Uniqueness error! \'{category}\' category is already registered.'
            elif not tech_stacks:
                msg = 'Failure! Tech stacks field should not be empty.'
            else:
                obj.category = category.lower()
                obj.tech_stacks = tech_stacks.lower()
                obj.save()
                msg = 'Trends Analytics updated successfully!'
                status_code = status.HTTP_200_OK
            return Response({"detail": msg}, status=status_code)
        except Exception as e:
            saveLogs(e)
            return Response({"detail": "Invalid Trend Analytics id"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        try:
            TrendsAnalytics.objects.get(id=pk).delete()
            return Response({'detail': 'Trend Analytics object deleted.'})
        except Exception as e:
            saveLogs(e)
            return Response({"detail": "Invalid Trend Analytics id"}, status=status.HTTP_406_NOT_ACCEPTABLE)