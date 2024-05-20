import datetime

from django.db.models import Count, Q, Func, F
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from tqdm import tqdm

from job_portal.models import JobArchive, Analytics, TechStats, JobDetail
# from collections import Counter
from scraper.utils.thread import start_new_thread
from utils.helpers import saveLogs


class ArchiveJobs(APIView):
    permission_classes = (AllowAny, )
    contract_onsite_enums = [
        "contract onsite",
        "contract on site",
        "contract"
    ]
    contract_remote_enums = [
        "contract remote",
    ]
    full_time_onsite_enums = [
        "full time onsite",
        "full time on site",
    ]
    full_time_remote_enums = [
        "full time remote",
        "remote",
        "full time"
    ]
    hybrid_full_time_enums = [
        "hybrid onsite",
        "hybrid on site",
        "hybrid full time",
        "hybrid remote",
    ]
    hybrid_contract_enums = [
        "hybrid contract"
    ]

    def get(self, request):
        message = "Only Admin has access to this endpoint!"
        if self.request.user.is_superuser:
            self.migrate_jobs_to_archive()
            message = "Job migration in progress!"
            return Response({"detail": message}, status=200)
        return Response({"detail": "Only Admin has access to this endpoint"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def migrate_jobs_to_archive(self, classify_data=None):
        try:
            last_30_days = datetime.datetime.now() - datetime.timedelta(days=30)
            if classify_data:
                query = Q()
                for item in classify_data.data_frame.itertuples():
                    query |= Q(company_name=item.company_name, job_title=item.job_title)
 
            jobs = JobDetail.objects.filter(created_at__gte=last_30_days, job_applied="not applied")
            filter_jobs = jobs.defer('job_description_tags')
            print(filter_jobs.count())
            print("filtered_jobs => ", jobs.count())
            if classify_data:
                jobs.filter(query)
            print("Started")
            bulk_data = [JobArchive(
                id=x.id,
                job_title=x.job_title,
                company_name=x.company_name,
                job_source=x.job_source,
                job_type=x.job_type,
                address=x.address,
                job_description=x.job_description,
                tech_keywords=x.tech_keywords,
                job_posted_date=x.job_posted_date,
                job_source_url=x.job_source_url,
                block=x.block,
                is_manual=x.is_manual,
                created_at=x.created_at,
                updated_at=x.updated_at
            ) for x in tqdm(filter_jobs.iterator())]
            #
            check = JobArchive.objects.bulk_create(bulk_data, ignore_conflicts=True, batch_size=500)
            print(check)
            jobs.delete()
            print("Terminated")

            self.save_analytics()
        except Exception as e:
            saveLogs(f"Exception in migrating data => {str(e)}")
            print("Exception in migrating data => ", e)

    """
    Scripts for creating analytics on basis of job archive model
    """
    def save_tech_stacks_stats(self, queryset, current_date):
        data = []
        expression = Func(F('tech_stacks'), function='unnest')
        tech_keywords = set(JobDetail.objects.only('tech_stacks').annotate(keywords=expression).values_list('keywords', flat=True))
        for x in tech_keywords:
            qs = queryset.filter(tech_keywords__icontains=x).aggregate(
                total=Count("id"),
                contract_on_site=Count('id', filter=Q(job_type__in=self.contract_onsite_enums)),
                contract_remote=Count('id', filter=Q(job_type__in=self.contract_remote_enums)),
                full_time_on_site=Count('id', filter=Q(job_type__in=self.full_time_onsite_enums)),
                full_time_remote=Count('id', filter=Q(job_type__in=self.full_time_remote_enums)),
                hybrid_full_time=Count('id', filter=Q(job_type__in=self.hybrid_full_time_enums)),
                hybrid_contract=Count('id', filter=Q(job_type__in=self.hybrid_contract_enums))
            )
            qs.update({"name": x, "job_posted_date": current_date})
            data.append(TechStats(**qs))
        TechStats.objects.bulk_create(data, ignore_conflicts=True, batch_size=500)

    def save_job_type_stats(self, queryset, current_date):
        job_types = [
            {"key": "Contract on site", "value": self.contract_onsite_enums},
            {"key": "Contract remote", "value": self.contract_remote_enums},
            {"key": "Full time on site", "value": self.full_time_onsite_enums},
            {"key": "Full time remote", "value": self.full_time_remote_enums},
            {"key": "Hybrid full time", "value": self.hybrid_full_time_enums},
            {"key": "Hybrid contract", "value": self.hybrid_contract_enums}
        ]
        data = [
            {
                "name": x['key'],
                "value": queryset.filter(job_type__in=x['value']).count(),
                "key": x['key'].lower().replace(" ", "_")
            }
            for x in job_types
        ]

        data = [Analytics(job_type=x['name'], jobs=x['value'], job_posted_date=current_date) for x in data]
        Analytics.objects.bulk_create(data, ignore_conflicts=True, batch_size=500)

    def save_analytics(self):
        fields = ['job_type', 'job_posted_date', 'tech_keywords', 'job_type']
        queryset = JobArchive.objects.only(*fields)
        current_date = datetime.datetime.now().date()
        qs = Analytics.objects.order_by('-job_posted_date').first()
        if qs:
            end_date = qs.job_posted_date.date()
        else:
            end_date = queryset.last().job_posted_date.date()
        # queryset.values_list()
        while current_date >= end_date:
            print(current_date, end_date)
            next_date = current_date - datetime.timedelta(days=1)
            daily_records = queryset.filter(job_posted_date__date=current_date)
            self.save_job_type_stats(daily_records, current_date)
            self.save_tech_stacks_stats(daily_records, current_date)

            current_date = next_date

        print("Script Terminated!")

# overall_tech = []
# last_30_days = datetime.datetime.now() - datetime.timedelta(days=29)
# data = JobArchive.objects.filter(job_posted_date__gte=last_30_days).values_list('tech_keywords', flat=True)
# for instance in data:
#     temp = instance.split(",")
#     for tech in temp:
#         overall_tech.append(tech)
# total_count = Counter(overall_tech)
# import pdb
# pdb.set_trace()

