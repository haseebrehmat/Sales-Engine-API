import calendar
from datetime import datetime, timedelta, date
from pprint import pprint

from django.db import models
from django.db.models import Count, F, Q, Value, Sum, FloatField, Avg
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractQuarter, Coalesce, Cast
from rest_framework.response import Response
from rest_framework.views import APIView
from job_portal.models import TrendsAnalytics, Analytics, TechStats
from job_portal.permissions.analytics import AnalyticsPermission


class GenerateAnalytics(APIView):
    permission_classes = (AnalyticsPermission,)
    queryset = Analytics.objects.all().order_by('-job_posted_date')
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

    def get(self, request):
        filters, start_date, end_date = self.filter_queryset(request)
        if not self.queryset.values_list("job_type", flat=True):
            return Response({"detail": "No Analytics Exists"}, status=406)
        self.tech_keywords = set(TechStats.objects.values_list("name", flat=True))
        self.job_types = set(self.queryset.values_list("job_type", flat=True))
        limit = int(request.GET.get("limit", 10))
        tech_stack_data, trending = self.get_tech_count_stats(start_date, end_date, limit)
        data = {
            "tech_stack_data": tech_stack_data,
            "trending": trending,
            "job_type_data": self.get_job_type_stats(),
            "filters": filters,
            "start_date": str(start_date.date()) if start_date else '',
            "end_date": str(end_date.date()) if end_date else '',
            "trend_analytics": self.get_trends_analytics(start_date, end_date),
            "tech_growth": self.check_tech_growth("python", start_date, end_date)
        }

        return Response(data)

    def get_tech_count_stats(self, start_date, end_date, limit=10):
        queryset = TechStats.objects.filter(job_posted_date__range=[start_date, end_date])

        data = queryset.filter(name__in=self.tech_keywords, job_posted_date__range=[start_date, end_date]).values(
            'name').annotate(
            total=Sum('total'),
            contract_on_site=Sum('contract_on_site'),
            contract_remote=Sum('contract_remote'),
            full_time_on_site=Sum('full_time_on_site'),
            full_time_remote=Sum('full_time_remote'),
            hybrid_full_time=Sum('hybrid_full_time'),
            hybrid_contract=Sum('hybrid_contract')
        )

        top_tech_stats = data.order_by('-total')[:limit]

        return data, top_tech_stats

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
        start_date = end_date = ""

        # if search_filter:
        #     self.queryset = self.queryset.filter(job_title__icontains=search_filter)

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
            month_days = calendar.monthrange(int(year), int(month))[-1]
            end_date = datetime.strptime(str_date, '%Y-%m-%d') + timedelta(days=month_days) - timedelta(seconds=1)
            self.queryset = self.queryset.annotate(
                month=ExtractMonth('job_posted_date'),
                year=ExtractYear('job_posted_date')).filter(month=month, year=year)

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

            self.queryset = (self.queryset.annotate(
                year=ExtractYear('job_posted_date'), quarter=ExtractQuarter('job_posted_date'))
            .filter(
                quarter=quarter_number, year=year
            ))
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
            self.queryset = self.queryset.annotate(year=ExtractYear('job_posted_date')).filter(year=year)
            data = {"months": [f"{year}-{'0' + str(x) if x < 10 else x}" for x in range(1, 13)]}

        else:
            format_string = "%Y-%m-%d"  # Replace with the format of your date string
            start_date = self.request.GET.get("start_date", "")
            end_date = self.request.GET.get("end_date", "")
            if start_date:
                start_date = datetime.strptime(start_date, format_string)
                self.queryset = self.queryset.filter(job_posted_date__gte=start_date)
            if end_date:
                end_date = datetime.strptime(end_date, format_string)
                calculated_end_date = end_date - timedelta(seconds=1)
                self.queryset = self.queryset.filter(job_posted_date__lte=calculated_end_date)

        if not start_date:
            start_date = self.queryset.last().job_posted_date if self.queryset.all() else ''
        if not end_date:
            end_date = self.queryset.first().job_posted_date if self.queryset.all() else ''

        return data, start_date, end_date

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

    def get_trends_analytics(self, start_date, end_date):
        try:
            trends_analytics = TrendsAnalytics.objects.all()
            data = []
            for trends in trends_analytics:
                # get stacks from trends analytics objects
                tech_stacks = trends.tech_stacks.split(',') if trends.tech_stacks else []
                # find job type stats of each trends analytics category
                queryset = TechStats.objects.filter(job_posted_date__range=[start_date, end_date])
                result = queryset.filter(name__in=tech_stacks, job_posted_date__range=[start_date, end_date]).values(
                    'id').aggregate(
                    total=Sum('total'),
                    contract_on_site=Sum('contract_on_site'),
                    contract_remote=Sum('contract_remote'),
                    full_time_on_site=Sum('full_time_on_site'),
                    full_time_remote=Sum('full_time_remote'),
                    hybrid_full_time=Sum('hybrid_full_time'),
                    hybrid_contract=Sum('hybrid_contract'),
                )
                result.update({'name': trends.category, 'tech_stacks': tech_stacks})
                data.append(result)
            return data
        except Exception as e:
            print("trend analytics failed due to ", e)
            return []

    def check_tech_growth(self, tech, start_date, end_date):
        queryset = TechStats.objects.filter(name__in=tech, job_posted_date__range=[start_date, end_date])
        data = queryset.filter(name__in=tech, job_posted_date__range=[start_date, end_date]).values('name').order_by(
            'job_posted_date__month').annotate(
            total=Sum('total'),
            contract_on_site=Sum('contract_on_site'),
            contract_remote=Sum('contract_remote'),
            full_time_on_site=Sum('full_time_on_site'),
            full_time_remote=Sum('full_time_remote'),
            hybrid_full_time=Sum('hybrid_full_time'),
            hybrid_contract=Sum('hybrid_contract'),
            month=F('job_posted_date__month'),
            year=F('job_posted_date__year')
        )
        return data

    def get_current_quarter(self):
        now = datetime.now()
        quarter = (now.month - 1) // 3 + 1
        return quarter, now.year

    def get_job_type_stats(self):
        data = [
            {
                "name": x,
                "value": self.queryset.filter(job_type__iexact=x).aggregate(count=Sum('jobs'))['count'],
                "key": x.lower().replace(" ", "_")
            }
            for x in self.job_types
        ]
        return data

# Generate Salary Range Graph
# class ExtractNumericValue(models.Func):
#     function = 'REGEXP_REPLACE'
#     template = "%(function)s(%(expressions)s, '[^0-9.]', '', 'g')"
#     output_field = FloatField()
#
#
# def calculate_salary_per_anum(salary):
#     if salary > 20000:
#         return float(salary)
#     elif salary > 1000:
#         return float(salary) * 12
#     else:
#         return float(salary) * 12 * 8 * 30
#
#
# salary_stats = []
# tech_keywords = set(JobDetail.objects.only('tech_keywords').values_list('tech_keywords', flat=True))
# fields = ['salary_max', 'salary_min', 'salary_format']
# for x in tech_keywords:
#     qs = JobDetail.objects.only(*fields)
#     max_salary = qs.filter(salary_max__isnull=False, tech_keywords=x).exclude(salary_max='').annotate(
#         numeric_amount=Cast(ExtractNumericValue('salary_max'), output_field=FloatField())
#     ).aggregate(average_salary=Coalesce(Avg('numeric_amount'), Value(0, output_field=FloatField())))['average_salary']
#     min_salary = qs.filter(salary_min__isnull=False, tech_keywords=x).exclude(salary_min='').annotate(
#         numeric_amount=Cast(ExtractNumericValue('salary_min'), output_field=FloatField())
#     ).aggregate(average_salary=Coalesce(Avg('numeric_amount'), Value(0, output_field=FloatField())))['average_salary']
#     if max_salary > 0:
#         salary_format = qs.first().salary_format
#         if not qs.first().salary_format:
#             max_salary = calculate_salary_per_anum(max_salary)
#             min_salary = calculate_salary_per_anum(min_salary)
#         salary_stats.append(
#             {
#                 "tech_stack": x,
#                 "max": round(max_salary, 2),
#                 "min": round(min_salary, 2),
#             }
#         )
#
#
# print(salary_stats)
