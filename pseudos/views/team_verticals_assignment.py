from pprint import pprint
from django.core import serializers
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from itertools import chain
from authentication.models import Profile
from authentication.serializers.team_management import TeamManagementSerializer
from job_portal.models import JobDetail, AppliedJobStatus
from job_portal.serializers.job_detail import JobDetailSerializer
from pseudos.models.verticals import Verticals
from authentication.models.team_management import Team
from authentication.models.user import User
from pseudos.models import Pseudos
from pseudos.serializers.pseudos import PseudoSerializer
from pseudos.serializers.verticals import VerticalSerializer


class TeamVerticalsAssignView(ListAPIView):  # class for assignment verticals to team
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
        for vertical in team.verticals.all():
            Verticals.objects.filter(id=vertical.id).update(assigned=False)
        team.verticals.clear()
        for vertical in all_verticals:
            if vertical.assigned == False:
                team.verticals.add(vertical)
                Verticals.objects.filter(id=vertical.id).update(assigned=True)
        status_code = status.HTTP_200_OK
        message = {"detail": "Verticals Saved Successfully"}
        return Response(message, status=status_code)


class UserVerticalsAssignView(APIView):  # class for assignment verticals to team members
    permission_classes = (AllowAny,)
    serializer_class = PseudoSerializer

    def get(self, request):  # New function for get complete team
        pk = request.query_params.get('team_id')
        team = Team.objects.filter(id=pk).first()
        vertical_id = team.verticals.values_list("id", flat=True)
        if team is not None:
            serializer = TeamManagementSerializer(team)
            data = serializer.data

            for x in data["members"]:
                verticals = Verticals.objects.filter(vertical__user__id=x["id"], id__in=vertical_id)
                if verticals.count() > 0:
                    temp = [
                        {"id": vertical.id, "name": vertical.name, "identity": vertical.identity,
                         "pseudo": vertical.pseudo.name}
                        for vertical in verticals]
                    x["verticals"] = temp

        else:
            data = []
        status_code = status.HTTP_200_OK
        return Response(data, status=status_code)

    def post(self, request):
        user_id = request.data.get('user_id')
        team_id = request.data.get('team_id')
        verticals = request.data.get('verticals')

        # fetching data from current team
        current_team = Team.objects.filter(id=team_id, members__id=user_id).first()

        # other team data
        other_teams = Team.objects.exclude(id=team_id)

        # User Profile
        profile = Profile.objects.filter(user_id=user_id).first()
        # Getting Vertical based on IDs
        verticals = Verticals.objects.filter(id__in=verticals)

        # getting current team vertical
        current_team_verticals = current_team.verticals.all()

        # getting other verticals
        other_vertical = []
        for team in other_teams:
            other_vertical.extend([team for team in team.verticals.all()])
        other_vertical.extend([x for x in verticals])
        for vertical in current_team_verticals:
            profile.vertical.remove(vertical)
        for v in verticals:
            profile.vertical.add(v)

        status_code = status.HTTP_200_OK
        message = {"detail": "Verticals Saved Successfully"}
        return Response(message, status=status_code)


class UserVerticals(APIView):
    def get(self, request):
        user_id = request.user.id
        job_id = request.GET.get("job_id")
        user_applied = AppliedJobStatus.objects.filter(applied_by=user_id, job_id=job_id)

        job = JobDetail.objects.filter(pk=job_id).first()
        profile = Profile.objects.filter(user_id=user_id).first()
        verticals = list(profile.vertical.values_list('id', flat=True))
        teams = Team.objects.filter(members__id=user_id).all()
        if len(verticals) == 0 or len(teams) == 0:
            data = []
        else:
            data = {"assigned": [{
                'id': team.id,
                'name': team.name,
                'verticals': [{"id": vertical.id, "name": vertical.name, "identity": vertical.identity}
                              for vertical in team.verticals.filter(id__in=verticals)]
            } for team in teams],
                "job": {
                    'id': job.id,
                    'name': job.job_title,
                    'company': job.company_name,
                    'type': job.job_type,
                    'description': job.job_description,
                    'source': job.job_source,
                    'link': job.job_source_url,
                    'posted_at': job.job_posted_date,
                },
                "history": [{
                    'vertical': apply.vertical.name,
                    "pseudo": apply.vertical.pseudo.name,
                    'time': apply.applied_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'team': apply.team.name,
                } for apply in user_applied]
            }
        return Response(data, status=status.HTTP_200_OK)


class JobVerticals(APIView):

    def get(self, request):
        user_id = request.GET.get("user_id")
        job_id = request.GET.get("job_id")
        job = JobDetail.objects.filter(id=job_id).first()
        serializer = JobDetailSerializer(job, many=False)

        user = User.objects.filter(id=user_id).first()
        verticals = user.profile.vertical.all()
        data = {"total_verticals": [{"name": x.name, "identity": x.identity, "id": x.id} for x in verticals]}
        data["total_verticals_count"] = len(data["total_verticals"])
        jobs = AppliedJobStatus.objects.filter(job_id=job_id, vertical__in=verticals)
        data["applied_verticals"] = [
            {"name": x.vertical.name, "identity": x.vertical.identity, "id": x.vertical.id}
            for x in jobs
        ]
        data["job_details"] = serializer.data
        data["total_applied_count"] = len(data["applied_verticals"])
        return Response(data, status=status.HTTP_200_OK)
