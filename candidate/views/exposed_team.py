from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from authentication.exceptions import InvalidUserException
from authentication.models.company import Company
from candidate.models import CandidateTeam, ExposedCandidate, ExposedCandidateTeam
from candidate.serializers.candidate_teams import CandidateTeamsSerializer
from candidate.serializers.exposed_candidate import ExposedCandidateSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors
class ExposedTeamListAPIView(APIView):
    serializer_class = ExposedCandidateSerializer
    def post(self, request):
        company_ids = request.data.get("company_ids", [])

        #here is the login of get all candidates from team
        team_ids = request.data.get("team_ids", [])
        candidate_ids = []
        data = []
        for team in team_ids:
            queryset = ExposedCandidateTeam.objects.filter(candidate_team_id=team)
            data = [x.exposed_candidate_id for x in queryset]
            [candidate_ids.append(x) for x in data]
        #here we need to remove duplicates from array
        candidate_ids = list(set(candidate_ids))
        candidate_ids = ','.join(str(value) for value in candidate_ids)
        candidate_ids = candidate_ids.split(",")

        #save exposed to companies ids in team exposed to feild
        for x in team_ids:
            team = CandidateTeam.objects.filter(pk=x).first()
            if team:
                team.exposed_to = company_ids
                team.save()
        if company_ids == [] or team_ids == []:
            message = "Team or Company should not be empty"
            status_code = status.HTTP_406_NOT_ACCEPTABLE
            return Response({"detail": message}, status_code)
        data = []
        for candidate_id in candidate_ids:
            candidate_id = ExposedCandidate.objects.filter(pk=candidate_id).first()
            candidate_id = candidate_id.candidate.id
            for company_id in company_ids:
                data.append(
                    {
                        "candidate_id": candidate_id,
                        "company_id": company_id,
                    }
                )
        instances = [ExposedCandidate(**item) for item in data]
        ExposedCandidate.objects.bulk_create(instances, ignore_conflicts=True)
        message = "Team Exposed Successfully"
        status_code = status.HTTP_200_OK
        return Response({"detail": message}, status_code)



