from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from candidate.models import Regions
from candidate.pagination.regions_pagination import RegionsPagination
from candidate.serializers.regions import RegionsSerializer


class RegionsListView(ListAPIView):
    serializer_class = RegionsSerializer
    pagination_class = RegionsPagination

    def get_queryset(self):
        search = self.request.query_params.get('search')
        queryset = Regions.objects.all()
        if search:
            queryset = queryset.filter(region__icontains=search)
        return queryset

    def post(self, request):
        name = request.data.get('name', '')
        if name:
            obj = Regions.objects.filter(region__iexact=name).first()
            if obj:
                msg = 'Region already exist!'
                status_code = status.HTTP_406_NOT_ACCEPTABLE
            else:
                Regions.objects.create(region=name)
                msg = 'Region created successfully!'
                status_code = status.HTTP_201_CREATED

        else:
            msg = 'Region name is missing!'
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response({'detail': msg}, status=status_code)


class AllRegions(APIView):
    def get(self, request):
        regions_list = [{'label': region.region, 'value': region.id} for region in Regions.objects.all()]
        return Response(regions_list)

class RegionsListDetailView(APIView):

    def get(self, request, pk):
        try:
            obj = Regions.objects.get(pk=pk)
            serializer = RegionsSerializer(obj, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Invalid region id'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, pk):
        try:
            name = request.data.get('name', '')
            obj = Regions.objects.get(pk=pk)
            obj.name = name
            obj.save()
            return Response({'detail': 'Region updated successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        try:
            Regions.objects.get(pk=pk).delete()
            return Response({'detail': 'Region deleted successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Invalid region id'}, status=status.HTTP_406_NOT_ACCEPTABLE)
