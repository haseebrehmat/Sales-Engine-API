import calendar
from datetime import datetime, timedelta, date
from pprint import pprint

from django.db.models import Count, F, Q, Value
from django.db.models.functions import ExtractMonth, ExtractYear
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from job_portal.models import JobDetail, JobArchive, TrendsAnalytics
from job_portal.permissions.analytics import AnalyticsPermission


class GenerateAnalytics(APIView):
    # job_archive = JobArchive.objects.all()
    queryset = JobArchive.objects.all()
    tech_keywords = ""
    job_types = ""
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
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
        filters, start_date, end_date = self.filter_queryset(request)
        self.tech_keywords = set(self.queryset.values_list("tech_keywords", flat=True))
        self.job_types = set(self.queryset.values_list("job_type", flat=True))

        data = {
            "tech_stack_data": self.get_tech_count_stats(),
            "job_type_data": self.get_job_type_stats(),
            "filters": filters,
            "start_date": str(start_date.date()) if start_date else '',
            "end_date": str(end_date.date()) if end_date else '',
            # "trend_analytics": self.get_trends_analytics(),
        }

        return Response(data)

    def get_tech_count_stats(self):
        data = []

        for x in self.tech_keywords:
            qs = self.queryset.filter(tech_keywords=x).aggregate(
                total=Count("id"),
                contract_on_site=Count('id', filter=Q(job_type__in=self.contract_onsite_enums)),
                contract_remote=Count('id', filter=Q(job_type__in=self.contract_remote_enums)),
                full_time_on_site=Count('id', filter=Q(job_type__in=self.full_time_onsite_enums)),
                full_time_remote=Count('id', filter=Q(job_type__in=self.full_time_remote_enums)),
                hybrid_full_time=Count('id', filter=Q(job_type__in=self.hybrid_full_time_enums)),
                hybrid_contract=Count('id', filter=Q(job_type__in=self.hybrid_contract_enums))
            )
            qs.update({"name": x})
            data.append(qs)

        return data

    def get_tech_counts(self, tech):
        data = [
            {
                "value": self.queryset.filter(tech_keywords=tech, job_type=x).count(),
                "key": x.lower().replace(" ", "_")
            }
            for x in self.job_types
        ]
        return data

    def filter_queryset(self, request):
        data = False
        search_filter = request.GET.get("search", "")
        year_filter = request.GET.get("year", "")
        quarter_filter = request.GET.get("quarter", "")
        month_filter = request.GET.get("month", "")
        week_filter = request.GET.get("week", "")

        if search_filter:
            self.queryset = self.queryset.filter(job_title__icontains=search_filter)

        if week_filter != "":
            filter = week_filter.split("-")
            year = filter[0]
            if filter[-1] in ["W" + str(x) if x < 10 else "W" + str(x) for x in range(1, 53)]:
                week = filter[-1].replace("W", "")

                str_date = str(year) + "-" + str(week) + "-" + str(1)
                start_date = datetime.strptime(str_date, "%Y-%W-%w")
                end_date = datetime.strptime(str_date, "%Y-%W-%w") + timedelta(days=8) - timedelta(seconds=1)
            self.queryset = self.queryset.filter(job_posted_date__range=[start_date, end_date])
            if month_filter:
                year, month = month_filter.split("-")
                data = {"week": self.get_week_numbers(year, month)}

        elif month_filter != "":

            year, month = month_filter.split("-")
            str_date = month_filter + "-" + "01"
            start_date = datetime.strptime(str_date, '%Y-%m-%d')
            month_days = 0
            month_days = calendar.monthrange(int(year), int(month))[-1]
            # else:  # February (Handling leap year condition)
            #     month_days = 29 if calendar.isleap(int(year)) else 28

            end_date = datetime.strptime(str_date, '%Y-%m-%d') + timedelta(days=month_days) - timedelta(seconds=1)
            self.queryset = self.queryset.annotate(
                month=ExtractMonth('created_at'),
                year=ExtractYear('created_at')).filter(month=month, year=year)

            if year_filter == "":
                data = {"weeks": self.get_week_numbers(year, month)}
            else:
                year = int(year_filter)
                quarter_number = int(quarter_filter.split("q")[-1])
                if quarter_number == 2:
                    quarter_number = 4
                elif quarter_number == 3:
                    quarter_number = 7
                elif quarter_number == 4:
                    quarter_number = 10

                start_date = datetime(year, quarter_number, 1)
                if quarter_filter == "q4":
                    end_date = datetime(year, 12, 31)
                else:
                    end_date = datetime(year, quarter_number + 3, 1) - timedelta(days=1)
                weeks = []
                for x in range(quarter_number, quarter_number + 3):
                    weeks.extend(self.get_week_numbers(year, x))

                data = {
                    "months": [
                        {
                            "value": f"{year}-{'0' + str(x) if x < 10 else x}",
                            "name": self.months[x - 1] + " " + str(year)
                        }
                        for x in range(quarter_number, quarter_number + 3)],
                    "weeks": weeks
                }

        elif quarter_filter != "" and year_filter != "":
            year = int(year_filter)
            quarter_number = int(quarter_filter.split("q")[-1])
            if quarter_number == 2:
                quarter_number = 4
            elif quarter_number == 3:
                quarter_number = 7
            elif quarter_number == 4:
                quarter_number = 10

            start_date = datetime(year, quarter_number, 1)
            if quarter_filter == "q4":
                end_date = datetime(year, 12, 31)
            else:
                end_date = datetime(year, quarter_number + 3, 1) - timedelta(days=1)

            self.queryset = self.queryset.filter(created_at__range=[start_date, end_date])
            weeks = []
            for x in range(quarter_number, quarter_number + 3):
                weeks.extend(self.get_week_numbers(year, x))

            data = {
                "months": [
                    {
                        "value": f"{year}-{'0' + str(x) if x < 10 else x}",
                        "name": self.months[x - 1] + " " + str(year)
                    }
                    for x in range(quarter_number, quarter_number + 3)],
                "weeks": weeks
            }

        elif year_filter != "":
            year = year_filter
            self.queryset = self.queryset.annotate(year=ExtractYear('created_at')).filter(year=year)
            data = {"months": [f"{year}-{'0' + str(x) if x < 10 else x}" for x in range(1, 13)]}

        else:
            format_string = "%Y-%m-%d"  # Replace with the format of your date string
            start_date = self.request.GET.get("start_date", "")
            end_date = self.request.GET.get("end_date", "")
            if start_date != "":
                # Convert the date string into a datetime object
                start_date = datetime.strptime(start_date, format_string)
                self.queryset = self.queryset.filter(created_at__gte=start_date)
            if end_date != "":
                end_date = datetime.strptime(end_date, format_string)
                calculated_end_date = end_date - timedelta(seconds=1)
                self.queryset = self.queryset.filter(created_at__lte=calculated_end_date)

        if start_date == "":
            start_date = self.queryset.last().job_posted_date if self.queryset.all() else ''
        if end_date == "":
            end_date = self.queryset.first().job_posted_date if self.queryset.all() else ''
        return data, start_date, end_date

    def get_job_type_stats(self):
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
                "value": self.queryset.filter(job_type__in=x['value']).count(),
                "key": x['key'].lower().replace(" ", "_")
            }
            for x in job_types
        ]
        return data

    def get_week_numbers(self, year, month):
        weeks = []
        year = int(year)
        month = int(month)
        start_date = date(year, month, 1)
        end_date = start_date + timedelta(days=31)  # Assuming maximum 31 days in a month

        current_date = start_date
        while current_date <= end_date:
            week_number = current_date.isocalendar()[1]  # Get the ISO week number
            if current_date.month == month:  # Only consider weeks within the specified month
                weeks.append({"name": "Week " + str(week_number), "value": f"{str(year)}-W{str(week_number)}"})
            current_date += timedelta(days=7)  # Move to the next week

        return weeks

    def get_trends_analytics(self):
        trends_analytics = TrendsAnalytics.objects.all()
        data = []
        for trends in trends_analytics:
            # get stacks from trends analytics objects
            tech_stacks = trends.tech_stacks.split(',') if trends.tech_stacks else []
            # find job type stats of each trends analytics category
            result = self.queryset.filter(tech_keywords__in=tech_stacks).aggregate(
                total=Count("id"),
                contract_on_site=Count('id', filter=Q(job_type__in=self.contract_onsite_enums)),
                contract_remote=Count('id', filter=Q(job_type__in=self.contract_remote_enums)),
                full_time_on_site=Count('id', filter=Q(job_type__in=self.full_time_onsite_enums)),
                full_time_remote=Count('id', filter=Q(job_type__in=self.full_time_remote_enums)),
                hybrid_full_time=Count('id', filter=Q(job_type__in=self.hybrid_full_time_enums)),
                hybrid_contract=Count('id', filter=Q(job_type__in=self.hybrid_contract_enums))
            )
            result.update({"name": trends.category})
            data.append(result)
        return data

#
# jobs = JobDetail.objects.filter(created_at__gte='2023-08-01')
# bulk_instances = [
#     JobArchive(
#         id=x.id,
#         job_title=x.job_title,
#         company_name=x.company_name,
#         job_source=x.job_source,
#         job_type=x.job_type,
#         address=x.address,
#         job_description=x.job_description,
#         tech_keywords=x.tech_keywords,
#         job_posted_date=x.job_posted_date,
#         job_source_url=x.job_source_url,
#         created_at=x.created_at,
#         updated_at=x.updated_at
#     )
#     for x in jobs]
# JobArchive.objects.bulk_create(bulk_instances, batch_size=500, ignore_conflicts=True)
