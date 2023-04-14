from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from authentication.serializers.team_management import TeamManagementSerializer
from pseudos.models.verticals import Verticals
from authentication.models.team_management import Team
from authentication.models.user import User
from pseudos.models import Pseudos
from pseudos.serializers.pseudos import PseudoSerializer


class TeamVerticalsAssignView(ListAPIView):         # class for assignment verticals to team
    permission_classes = (IsAuthenticated,)
    serializer_class = PseudoSerializer

    def get_queryset(self):
        company_id = self.request.user.profile.company.id
        return Pseudos.objects.filter(company_id=company_id)

    def post(self, request):
        team = request.data.get('team_id')
        team = Team.objects.filter(id=team).first()
        all_verticals = request.data.get('verticals')
        all_verticals = Verticals.objects.filter(id__in=all_verticals)
        for instance in team.verticals.all():
            team.verticals.remove(instance)
        for vertical in all_verticals:
            team.verticals.add(vertical)
        status_code = status.HTTP_200_OK
        message = {"detail": "Verticals Assignment Successfully"}
        return Response(message, status=status_code)


class UserVerticalsAssignView(ListAPIView):            # class for assignment verticals to team members
    permission_classes = (AllowAny,)
    serializer_class = PseudoSerializer

    def get(self, request):                             # New function for get complete team
        pk = request.query_params.get('team_id')
        team = Team.objects.filter(id=pk).first()
        serializer = TeamManagementSerializer(team)
        status_code = status.HTTP_200_OK
        return Response(serializer.data, status=status_code)

    def post(self, request):
        user = request.data.get('user_id')
        user = User.objects.filter(id=user).first()
        verticals = request.data.get('verticals')
        verticals = Verticals.objects.filter(id__in=verticals)
        for instance in user.vertical.all():
            user.vertical.remove(instance)
        for instance in verticals:
            user.vertical.add(instance)
        status_code = status.HTTP_200_OK
        message = {"detail": "Verticals Assignment Successfully"}
        return Response(message, status=status_code)
