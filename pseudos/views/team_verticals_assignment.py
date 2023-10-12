from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import Profile, UserRegions, Role, MultipleRoles
from authentication.serializers.team_management import TeamManagementSerializer
from job_portal.models import JobDetail, AppliedJobStatus, BlacklistJobs, RestrictVertical
from job_portal.serializers.job_detail import JobDetailSerializer
from pseudos.models.verticals import Verticals
from authentication.models.team_management import Team, TeamRoleVerticalAssignment
from authentication.models.user import User
from pseudos.models import Pseudos
from pseudos.serializers.pseudos import PseudoSerializer
from pseudos.serializers.verticals import VerticalSerializer
from pseudos.models.verticals_regions import VerticalsRegions


class TeamVerticalsAssignView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PseudoSerializer

    def get_queryset(self):
        company_id = self.request.user.profile.company.id
        return Pseudos.objects.filter(company_id=company_id)

    def post(self, request):
        team = request.data.get('team_id')
        team = Team.objects.filter(id=team).first()
        all_verticals = request.data.get('verticals')
        team_assign_verticals = TeamRoleVerticalAssignment.objects.filter(team=team)
        all_verticals = Verticals.objects.filter(id__in=all_verticals)
        excluded_ids = []
        for vertical in team.verticals.all():
            Verticals.objects.filter(id=vertical.id).update(assigned=False)
        team.verticals.clear()
        for vertical in all_verticals:
            excluded_ids.append(vertical.id)
            if vertical.assigned == False:
                team.verticals.add(vertical)
                Verticals.objects.filter(id=vertical.id).update(assigned=True)
        team_assign_verticals.exclude(vertical_id__in=excluded_ids).delete()
        status_code = status.HTTP_200_OK
        message = {"detail": "Verticals Saved Successfully"}
        return Response(message, status=status_code)


# class for assignment verticals to team members
class UserVerticalsAssignView(APIView):
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
                try:
                    verticals = Verticals.objects.filter(vertical__user__id=x["id"], id__in=vertical_id)
                    if verticals:
                        verticals_serializer = VerticalSerializer(verticals, many=True)
                        x["verticals"] = verticals_serializer.data
                except:
                    print("No Verticals")
                multiple_roles = MultipleRoles.objects.filter(user_id=x['id']).count()
                if multiple_roles > 0:
                    assign_roles = TeamRoleVerticalAssignment.objects.filter(
                        member_id=x['id'],
                        team_id=pk
                    ).values_list("role_id", flat=True)
                    x["allow_assignment"] = not multiple_roles == len(set(assign_roles))
                else:
                    x["allow_assignment"] = True


        else:
            data = []
        status_code = status.HTTP_200_OK
        return Response(data, status=status_code)

    def post(self, request):
        user_id = request.data.get('user_id')
        team_id = request.data.get('team_id')
        verticals = request.data.get('verticals')
        role_id = request.data.get('role_id')

        if not role_id:
            return Response({"detail": "Roles cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)

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
        invalid_verticals = 0
        # removing previously assign verticals
        TeamRoleVerticalAssignment.objects.filter(
            team_id=team_id,
            member_id=user_id,
            role_id=role_id
        ).delete()
        for v in verticals:
            if self.is_valid_vertical(v, profile.user):
                profile.vertical.add(v)

                # assigning vertical to the team along with its roles
                TeamRoleVerticalAssignment.objects.create(
                    vertical=v,
                    team_id=team_id,
                    member_id=user_id,
                    role_id=role_id
                )
            else:
                invalid_verticals += 1
        error_msg = f'Except {invalid_verticals} verticals due to invalid regions.' if invalid_verticals > 0 else ''
        status_code = status.HTTP_200_OK
        message = {"detail": "Verticals Saved Successfully!" + f' {error_msg}'}
        return Response(message, status=status_code)

    def is_valid_vertical(self, vertical, user):
        verticals_regions_set = set(
            VerticalsRegions.objects.filter(verticals=vertical).values_list('region', flat=True))
        user_regions_set = set(UserRegions.objects.filter(user=user).values_list('region', flat=True))
        result = verticals_regions_set.intersection(user_regions_set)
        return True if result else False


class UserVerticals(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            job_id = request.GET.get("job_id")
            user_applied = AppliedJobStatus.objects.filter(applied_by=user_id, job_id=job_id)

            job = JobDetail.objects.filter(pk=job_id).first()
            profile = Profile.objects.filter(user_id=user_id).first()
            verticals = list(profile.vertical.values_list('id', flat=True))
            team_ids = (TeamRoleVerticalAssignment.objects.filter(role_id=request.user.roles_id, member_id=user_id)
                        .values_list("team_id", flat=True))
            teams = Team.objects.filter(id__in=team_ids)

            if len(verticals) == 0 or len(teams) == 0:
                data = []
            else:
                data = {
                    "assigned": [
                        {
                            'id': team.id,
                            'name': team.name,
                            'verticals': [
                                {
                                    "id": vertical.id,
                                    "name": vertical.name,
                                    "identity": vertical.identity,
                                    "applied_status": True if RestrictVertical.objects.filter(vertical=vertical.id, company_name=job.company_name).exists() else False,
                                } for vertical in self.get_verticals(team.id, request)
                            ]
                        } for team in teams
                    ],
                    "job": {
                        'id': job.id,
                        'name': job.job_title,
                        'company': job.company_name,
                        'type': job.job_type,
                        'description': job.job_description,
                        'source': job.job_source,
                        'link': job.job_source_url,
                        'posted_at': job.job_posted_date
                    },
                    "history": [
                        {
                            'vertical': apply.vertical.name,
                            "pseudo": apply.vertical.pseudo.name,
                            'time': apply.applied_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'team': apply.team.name
                        } for apply in user_applied]}

            status_code = status.HTTP_200_OK
        except Exception as e:
            data = {'detail': str(e)}
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(data, status=status_code)

    def get_verticals(self, team_id, request):
        vertical_ids = TeamRoleVerticalAssignment.objects.filter(
            team_id=team_id,
            role_id=request.user.roles_id
        ).values_list('vertical_id', flat=True)
        return Verticals.objects.filter(id__in=vertical_ids)


class JobVerticals(APIView):

    def get(self, request):
        user_id = request.GET.get("user_id")
        job_id = request.GET.get("job_id")
        job = JobDetail.objects.filter(id=job_id).first()
        job.block = self.is_job_block(request, job)
        serializer = JobDetailSerializer(job, many=False)
        user = User.objects.filter(id=user_id).first()
        verticals = user.profile.vertical.all()
        data = {"total_verticals": [{"name": x.name, "identity": x.identity, "id": x.id} for x in verticals]}
        data["total_verticals_count"] = len(data["total_verticals"])
        jobs = AppliedJobStatus.objects.filter(job_id=job_id, vertical__in=verticals)
        data["applied_verticals"] = [{"name": x.vertical.name, "identity": x.vertical.identity, "id": x.vertical.id} for
                                     x in jobs]
        data["job_details"] = serializer.data
        data["total_applied_count"] = len(data["applied_verticals"])
        return Response(data, status=status.HTTP_200_OK)

    def get_blacklist_companies(self, request):
        if request.user.profile.company:
            company = request.user.profile.company
            blacklist_companies = list(
                BlacklistJobs.objects.filter(company_id=company.id).values_list("company_name", flat=True))
        else:
            blacklist_companies = list(BlacklistJobs.objects.all().values_list("company_name", flat=True))
        blacklist_companies = [c.lower() for c in blacklist_companies if c]
        return blacklist_companies

    def is_job_block(self, request, job):
        flag = job.company_name in self.get_blacklist_companies(request)
        return flag
