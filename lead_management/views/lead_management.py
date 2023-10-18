import datetime

from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from authentication.models import Team
from candidate.utils.custom_pagination import LeadManagementPagination, LeadManagementDataPagination
from job_portal.models import AppliedJobStatus
from job_portal.serializers.restrict_verticals import RestrictVerticalSerializer
from lead_management.models import Lead, CompanyStatus, LeadActivity, LeadActivityNotes
from lead_management.serializers import LeadSerializer
from lead_management.serializers.lead_management_serializer import LeadManagementSerializer, CustomLeadSerializer
from settings.utils.helpers import serializer_errors


class StatusLeadManagement(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = LeadManagementPagination
    serializer_class = LeadManagementSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['company__name', 'status__name']

    def get_queryset(self):
        role = str(self.request.user.roles)
        start_date = self.request.GET.get("start_date", False)
        end_date = self.request.GET.get("end_date", False)
        if "owner" in role.lower():
            queryset = CompanyStatus.objects.filter(company=self.request.user.profile.company).exclude(status=None)
        else:
            queryset = CompanyStatus.objects.filter(company=self.request.user.profile.company).exclude(status=None)
        if start_date and end_date:
            format_string = "%Y-%m-%d"  # Replace with the format of your date string

            # Convert the date string into a datetime object
            start_date = datetime.datetime.strptime(start_date, format_string)
            end_date = datetime.datetime.strptime(end_date, format_string) - datetime.timedelta(seconds=1)
            queryset = queryset.filter(updated_at__range=[start_date, end_date])
        queryset = queryset.order_by("updated_at")
        return queryset


    def post(self, request):
        # if CompanyStatus.objects.filter(pk=request.data.get('status', '')).first().status.name == 'hired':
        #     applied_job_status = AppliedJobStatus.objects.filter(pk=request.data.get('job', '')).first()
        #     vertical_id = applied_job_status.vertical_id
        #     company = applied_job_status.job.company_name
        #     data = {"company_name": company, "vertical": vertical_id}
        #     serializer = RestrictVerticalSerializer(data=data, many=False)
        #     if serializer.is_valid():
        #         data = serializer.validated_data
        #         serializer.create(data)
        #     else:
        #         msg = {'detail': 'Already hired with this vertical in this company'}
        #         status_code = status.HTTP_406_NOT_ACCEPTABLE
        #         return Response(msg, status=status_code)

        data, status_code = self.convert_to_lead(request)
        return Response(data, status=status_code)

    @transaction.atomic
    def convert_to_lead(self, request):
        serializer = LeadSerializer(data=request.data, many=False)
        try:
            if serializer.is_valid():
                applied_job_status = request.data.get('job')
                company_status = request.data.get('status')
                phase = request.data.get('phase')
                effect_date = request.data.get('effect_date')
                due_date = request.data.get('due_date')
                notes = request.data.get('notes')
                candidate = request.data.get('candidate')

                # convert to lead
                lead = Lead.objects.create(applied_job_status_id=applied_job_status, company_status_id=company_status,
                                           phase_id=phase, candidate_id=candidate, converter=request.user)
                
                # here is a logic of create object in restrict_vertical
                if CompanyStatus.objects.filter(pk=company_status).first().status.name == 'hired':
                    company_name = lead.applied_job_status.job.company_name
                    vertical = lead.applied_job_status.vertical_id
                    data = {"company_name": company_name, "vertical": vertical}
                    serializer = RestrictVerticalSerializer(data=data, many=False)
                    if serializer.is_valid():
                        data = serializer.validated_data
                        serializer.create(data)
                    else:
                        raise ValidationError({"detail": "You have already hired in this company"}, code=406)
                        
                # change applied job for applied job
                AppliedJobStatus.objects.filter(id=applied_job_status)\
                    .update(is_converted=True, converted_at=datetime.datetime.now())

                # create a new activity for lead
                lead_activity = LeadActivity.objects.create(lead_id=lead.id, company_status_id=company_status,
                                                            phase_id=phase, candidate_id=candidate)
                if effect_date:
                    lead_activity.effect_date = effect_date
                if due_date:
                    lead_activity.due_date = due_date
                lead_activity.save()

                if notes:
                    LeadActivityNotes.objects.create(lead_activity=lead_activity, message=notes, user=request.user)
                msg = {'detail': 'Lead Converted successfully!'}
                status_code = status.HTTP_201_CREATED
            else:
                msg = {'detail': serializer_errors(serializer)}
                status_code = status.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            msg = {'detail': str(e)}
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return msg, status_code


class LeadManagement(ListAPIView):
    queryset = Lead.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = LeadManagementDataPagination
    serializer_class = CustomLeadSerializer
    filter_backends = [SearchFilter]
    search_fields = ['company_status__status__name', 'phase__name',
                     'applied_job_status__job__job_title', 'applied_job_status__job__company_name']

    def get_queryset(self):
        company = self.request.user.profile.company
        self.queryset = self.queryset.filter(company_status__company=company)
        self.queryset = self.apply_filters(self.request, self.queryset)
        return self.queryset.order_by("updated_at")

    def apply_filters(self, request, queryset):
        role = request.user.roles.name
        user = [str(request.user.id)]
        current_user = request.user

        if len(Team.objects.filter(reporting_to__in=user)) > 0:
            user.extend(
                [str(x) for x in Team.objects.filter(reporting_to__id__in=user).values_list("members__id", flat=True)])

        stacks = request.query_params.get('stacks', '')
        from_date = request.query_params.get('from', '')
        to_date = request.query_params.get('to', '')
        members = request.query_params.get('members', '')
        team = request.query_params.get('team', '')
        candidates = request.query_params.get('candidates', None)
        status = request.query_params.get('status', '')
        phase = request.query_params.get('phase', '')

        stacks_query = Q()
        from_date_query = Q()
        to_date_query = Q()
        members_query = Q()
        team_query = Q()
        candidate_query = Q()
        status_query = Q()
        phase_query = Q()

        if stacks:
            stacks_query = Q(applied_job_status__job__tech_keywords__in=stacks.split(','))

        if from_date:
            from_date_query = Q(updated_at__gte=datetime.datetime.strptime(from_date, "%Y-%m-%d").date())

        if to_date:
            to_date_query = Q(
                updated_at__lt=datetime.datetime.strptime(to_date, "%Y-%m-%d").date() + datetime.timedelta(days=1))

        if team:
            team_query = Q(applied_job_status__team__id=team)

        else:
            if 'owner' not in role.lower():
                user_team = Team.objects.filter(reporting_to=current_user)
                if user_team:
                    team_query = Q(applied_job_status__team__id__in=list(user_team.values_list('id', flat=True)))
                else:
                    team_query = Q(applied_job_status__applied_by=current_user)

        if members:
            members = members.split(',')
            members_query = Q(applied_job_status__applied_by__id__in=members)

        if candidates:
            candidate_query = Q(candidate__id__in=candidates.split(','))

        if status:
            status_query = Q(company_status__id=status)
        if phase:
            phase_query = Q(phase__id=phase)

        data = (queryset.filter(team_query) | Lead.objects.filter(converter=current_user) |
                Lead.objects.filter(candidate__email=current_user.email))
        queryset = data.filter(members_query, stacks_query, from_date_query, to_date_query, candidate_query,
                               status_query, phase_query)
        return queryset
