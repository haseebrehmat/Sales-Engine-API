from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pseudos.models import SectionStatus, Verticals
from pseudos.serializers.sectionstatus import SectionStatusSerializer

class SectionStatusView(APIView):
    #permission_classes = (VerticalPermissions,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SectionStatusSerializer
    def post(self, request, pk):
        data = request.data
        vertical_id = Verticals.objects.filter(pk=pk).first()
        for key, value in data.items():
            conditions = [
                value["name"] != "",
                value["name"] is not None,
                value["status"] != "",
                value["status"] is not None,
            ]
            if not all(conditions):
                return Response({"detail": f"Fields cannot be empty in {key} section"},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            section, created = SectionStatus.objects.update_or_create(
                code=key,
                vertical=vertical_id,
                defaults={
                    "name": value["name"],
                    "status": value["status"],
                }
            )

            SectionStatusSerializer(section)
        # data = request.data
        # print(data['skill']['name'])
        # for key, value in data.items():
        #     conditions = [
        #         value["name"] != "",
        #         value["name"] != None,
        #         value["status"] != "",
        #         value["status"] != None,
        #     ]
        #     if not all(conditions):
        #         return Response({f'detail": "Fields cannot be empty in {key} section'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        #     try:
        #         instance = get_object_or_404(SectionStatus.objects.all(), code=key)
        #         serializer = SectionStatusSerializer(instance,
        #                                  data={
        #                                      "name": value["name"],
        #                                      "status": value["status"],
        #                                  },
        #                                  partial=True,
        #                                              )
        #         if serializer.is_valid():
        #             serializer.save()
        #     except:
        #         serializer = SectionStatusSerializer(data={
        #                                      "code": key,
        #                                      "name": value["name"],
        #                                      "status": value["status"],
        #                                  },
        #                                  many=False,)
        #         if serializer.is_valid():
        #             serializer.create(serializer.data)
        message = "Section Info Saved Successfully"
        status_code = status.HTTP_200_OK
        return Response({"detail": message}, status_code)
