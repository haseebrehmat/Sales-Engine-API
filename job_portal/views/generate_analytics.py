import calendar
import math
from datetime import datetime, timedelta, date

from django.db.models import F, Sum
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractQuarter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from job_portal.models import TrendsAnalytics, Analytics, TechStats


class GenerateAnalytics(APIView):
    # permission_classes = (AnalyticsPermission,)
    permission_classes = (AllowAny,)
    queryset = Analytics.objects.all().order_by('-job_posted_date')
    excluded_techs = []
    tech_keywords = ""
    job_types = ""
    percentage = None
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
        self.percentage = request.GET.get('percent')
        if self.percentage:
            self.percentage = (100 + float(self.percentage)) / 100
        else:
            self.percentage = 1
        self.excluded_techs = request.GET.get('excluded_techs', [])
        filters, start_date, end_date = self.filter_queryset(request)
        if not self.queryset.values_list("job_type", flat=True):
            return Response({"detail": "No Analytics Exists"}, status=406)
        self.tech_keywords = set(TechStats.objects.values_list("name", flat=True))
        if self.excluded_techs and self.tech_keywords:
            self.excluded_techs = self.excluded_techs.split(',')
            self.tech_keywords = self.tech_keywords.difference(set(self.excluded_techs))
        self.job_types = set(self.queryset.values_list("job_type", flat=True))
        limit = int(request.GET.get("limit", 10))
        tech_stack_data, trending = self.get_tech_count_stats(start_date, end_date, limit)
        data = {
            "tech_stack_data": tech_stack_data,
            "trending": trending,
            "job_type_data": self.get_job_type_stats(start_date, end_date),
            "filters": filters,
            "start_date": str(start_date.date()) if start_date else '',
            "end_date": str(end_date.date()) if end_date else '',
            "trend_analytics": self.get_trends_analytics(start_date, end_date),
            "tech_growth": self.check_tech_growth("python", start_date, end_date),
            "quarterly_trends": self.get_quarterly_trends(start_date),
            "monthly_trends": self.get_monthly_trends(start_date),
            "monthly_tech_data": self.get_monthly_tech_data(start_date),
            "quarterly_tech_data": self.get_quarterly_tech_data(start_date),
            "quarterly_job_types": self.get_quarterly_job_types(start_date),
            "montly_job_types": self.get_monthly_job_types(start_date),
        }
        return Response(data)

    def get_tech_count_stats(self, start_date, end_date, limit=10):
        queryset = TechStats.objects.filter(name__in=self.tech_keywords, job_posted_date__range=[start_date, end_date])
        data = []
        top_tech_stats = []
        if queryset:
            data = queryset.values(
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

            total_expression = lambda x: [value for key, value in x.items() if
                                          isinstance(value, int) and key != 'total']
            expression = lambda x: {
                key: math.ceil(self.percentage * value) if isinstance(value, int) else value
                for key, value in x.items()
            }
            data = [{**expression(x)} for x in data]
            data = [{**x, 'total': sum(total_expression(x))} for x in data]

            top_tech_stats = [{**expression(x)} for x in top_tech_stats]
            top_tech_stats = [{**x, 'total': sum(total_expression(x))} for x in top_tech_stats]
        return data, top_tech_stats

    def get_tech_counts(self, tech):
        queryset = self.queryset.filter(tech_keywords=tech)
        data = [
            {
                "value": math.ceil(self.percentage * queryset.filter(job_type=x).count()) if queryset else 0,
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
                year=ExtractYear('job_posted_date'), quarter=ExtractQuarter('job_posted_date')).filter(
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
                queryset = TechStats.objects.filter(name__in=tech_stacks, job_posted_date__range=[start_date, end_date])
                result = queryset.values(
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
                total_expression = lambda x: [value for key, value in x.items() if
                                              isinstance(value, int) and key != 'total']
                expression = lambda x: {
                    key: math.ceil(self.percentage * value) if isinstance(value, int) else value
                    for key, value in x.items()
                }
                result = expression(result)
                result.update({'total': sum(total_expression(result))})
                data.append(result)
            return data
        except Exception as e:
            print("trend analytics failed due to ", e)
            return []

    def check_tech_growth(self, tech, start_date, end_date):
        data = []
        try:
            queryset = TechStats.objects.filter(name__in=tech, job_posted_date__range=[start_date, end_date])
            if queryset:
                data = queryset.values(
                    'name').order_by(
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
                if data:
                    total_expression = lambda x: [value for key, value in x.items() if
                                                  isinstance(value, int) and key != 'total']
                    expression = lambda x: {
                        key: math.ceil(self.percentage * value) if isinstance(value, int) else value
                        for key, value in x.items()
                    }
                    result = expression(data)
                    result.update({'total': sum(total_expression(result))})

                    data = [result]
        except Exception as e:
            data = []
        return data

    def get_current_quarter(self):
        now = datetime.now()
        quarter = (now.month - 1) // 3 + 1
        return quarter, now.year

    def get_job_type_stats(self, start_date, end_date):
        qs = None
        if self.excluded_techs:
            qs = TechStats.objects.filter(name__in=self.excluded_techs,
                                          job_posted_date__range=[start_date, end_date])
            if qs:
                qs = qs.aggregate(
                contract_remote=Sum('contract_remote'), full_time_remote=Sum('full_time_remote'),
                hybrid_contract=Sum('hybrid_contract'), full_time_on_site=Sum('full_time_on_site'),
                hybrid_full_time=Sum('hybrid_full_time'), contract_on_site=Sum('contract_on_site'))

        caculated_value = lambda x, exclude_count: math.ceil(self.percentage * (abs(x - exclude_count)))

        data = []

        for x in self.job_types:
            key = x.lower().replace(" ", "_")
            jobs_count = self.queryset.filter(job_type__iexact=x).aggregate(count=Sum('jobs'))['count']
            excluded_jobs_count = qs[key] if qs else 0
            obj = {
                "name": x,
                "value": caculated_value(jobs_count, excluded_jobs_count),
                "key": key
            }
            data.append(obj)
        return data

    def get_quarterly_trends(self, date):
        data = []
        try:
            year = date.year
            trends_analytics = TrendsAnalytics.objects.all()
            values_list = []
            for x in trends_analytics:

                tech_stacks = x.tech_stacks.split(',') if x.tech_stacks else []

                for quarter in range(1, 5):
                    qs = TechStats.objects.annotate(
                        year=ExtractYear('job_posted_date'),
                        quarter=ExtractQuarter('job_posted_date'),
                    ).filter(
                        quarter=quarter, year=year, name__in=tech_stacks
                    )

                    if qs:
                        qs = qs.aggregate(total=Sum('total'))
                        values_list.append(math.ceil(self.percentage * qs['total']))
                        data.append(
                            {
                                f'q{quarter}': math.ceil(self.percentage * qs['total']),
                                'category': x.category
                            }
                        )
            result_list = []
            merged_dict = {}
            for d in data:
                category = d["category"]
                d.pop("category")

                if category in merged_dict:
                    merged_dict[category].update(d)
                else:
                    merged_dict[category] = d

            for category, data in merged_dict.items():
                data["category"] = category
                result_list.append(data)

            data = {'data': result_list, 'min_value': min(values_list), 'max_value': max(values_list)}
        except Exception as e:
            data = None
        return data

    def get_monthly_trends(self, date):
        data = []
        try:
            year = date.year
            trends_analytics = TrendsAnalytics.objects.all()
            values_list = []
            for x in trends_analytics:

                tech_stacks = x.tech_stacks.split(',') if x.tech_stacks else []

                for idx, month in enumerate(self.months):
                    qs = TechStats.objects.annotate(
                        year=ExtractYear('job_posted_date'),
                        month=ExtractMonth('job_posted_date'),
                    ).filter(
                        month=idx + 1, year=year, name__in=tech_stacks
                    )

                    if qs:
                        qs = qs.aggregate(total=Sum('total'))
                        total = math.ceil(self.percentage * qs['total'])
                    else:
                        total = 0
                    data.append(
                        {
                            month.lower(): total,
                            'category': x.category
                        }
                    )
                    values_list.append(total)
            result_list = []
            merged_dict = {}

            for d in data:
                category = d["category"]
                d.pop("category")

                if category in merged_dict:
                    merged_dict[category].update(d)
                else:
                    merged_dict[category] = d

            for category, data in merged_dict.items():
                data["category"] = category
                result_list.append(data)
            data = {'data': result_list, 'min_value': min(values_list), 'max_value': max(values_list)}
        except Exception as e:
            data = []
        return data

    def get_monthly_tech_data(self, date):
        data = []
        try:
            year = date.year
            values_list = []
            for idx, month in enumerate(self.months):
                month_number = idx + 1
                month = month.lower()
                qs = TechStats.objects.annotate(
                    year=ExtractYear('job_posted_date'),
                    month=ExtractMonth('job_posted_date'),
                ).filter(
                    month=month_number, year=year, name__in=self.tech_keywords
                ).values('name').annotate(total_jobs=Sum('total')).values('name', 'total_jobs')
                obj_exp = lambda x: ({
                                         'name': x['name'],
                                         month: math.ceil(self.percentage * x['total_jobs'])
                                     }, values_list.append(math.ceil(self.percentage * x['total_jobs'])))[0]
                data.extend(obj_exp(x) for x in qs)
            result_list = []
            merged_dict = {}

            for d in data:
                name = d["name"]
                d.pop("name")

                if name in merged_dict:
                    merged_dict[name].update(d)
                else:
                    merged_dict[name] = d

            min_value = min(values_list)
            for name, data in merged_dict.items():
                for month in self.months:
                    if month.lower() not in data.keys():
                        data[month.lower()] = 0
                        min_value = 0
                data["name"] = name
                result_list.append(data)
            data = {'data': result_list, 'min_value': min_value, 'max_value': max(values_list)}
        except Exception as e:
            data = []
        return data

    def get_quarterly_tech_data(self, date):
        data = []
        try:
            year = date.year
            values_list = []
            for quarter in range(1, 5):
                qs = TechStats.objects.annotate(
                    year=ExtractYear('job_posted_date'),
                    quarter=ExtractQuarter('job_posted_date'),
                ).filter(
                    quarter=quarter, year=year, name__in=self.tech_keywords
                ).values('name').annotate(total_jobs=Sum('total')).values('name', 'total_jobs')
                quarter_obj_exp = lambda x: \
                    (values_list.append(math.ceil(self.percentage * x['total_jobs'])),
                     {'name': x['name'], 'q' + str(quarter): math.ceil(self.percentage * x['total_jobs'])})[-1]
                data.extend([quarter_obj_exp(x) for x in qs])
            result_list = []
            merged_dict = {}

            for d in data:
                name = d["name"]
                d.pop("name")

                if name in merged_dict:
                    merged_dict[name].update(d)
                else:
                    merged_dict[name] = d

            quarters = ['q1', 'q2', 'q3', 'q4']
            min_value = min(values_list)
            for name, data in merged_dict.items():
                for q in quarters:
                    if q not in data.keys():
                        data[q] = 0
                        min_value = 0
                data["name"] = name
                result_list.append(data)
            data = {'data': result_list, 'min_value': min_value, 'max_value': max(values_list)}
        except Exception as e:
            data = []
        return data

    def get_quarterly_job_types(self, date):
        data_obj = []
        try:
            year = date.year
            for quarter in range(1, 5):
                qs = None
                if self.excluded_techs:
                    qs = TechStats.objects.annotate(quarter=ExtractQuarter('job_posted_date')).filter(
                        name__in=self.excluded_techs,
                        quarter=quarter)
                    if qs:
                        qs = qs.aggregate(
                            contract_remote=Sum('contract_remote'), full_time_remote=Sum('full_time_remote'),
                            hybrid_contract=Sum('hybrid_contract'), full_time_on_site=Sum('full_time_on_site'),
                            hybrid_full_time=Sum('hybrid_full_time'), contract_on_site=Sum('contract_on_site'))

                caculated_value = lambda x, exclude_count: math.ceil(self.percentage * (abs(x - exclude_count)))
                data = []
                for x in self.job_types:
                    key = x.lower().replace(" ", "_")
                    obj = {
                        "name": x,
                        "value": 0,
                        "key": key
                    }
                    query_result = self.queryset.annotate(
                        quarter=ExtractQuarter('job_posted_date'),
                        year=ExtractYear('job_posted_date')
                    ).filter(
                        job_type__iexact=x,
                        quarter=quarter,
                        year=year
                    )
                    if query_result:
                        jobs_count = query_result.aggregate(count=Sum('jobs'))['count']
                        excluded_jobs_count = qs[key] if qs else 0
                        obj.update({'value': caculated_value(jobs_count, excluded_jobs_count)})
                    data.append(obj)
                data_obj.append(data)
        except Exception as e:
            data_obj = []
            print(e)
        return data_obj

    def get_monthly_job_types(self, date):
        data_obj = []
        try:
            year = date.year
            for idx, month in enumerate(self.months):
                month_number = idx + 1
                qs = None
                if self.excluded_techs:
                    qs = TechStats.objects.annotate(month=ExtractMonth('job_posted_date')).filter(
                        name__in=self.excluded_techs,
                        month=month_number)
                    if qs:
                        qs = qs.aggregate(
                            contract_remote=Sum('contract_remote'), full_time_remote=Sum('full_time_remote'),
                            hybrid_contract=Sum('hybrid_contract'), full_time_on_site=Sum('full_time_on_site'),
                            hybrid_full_time=Sum('hybrid_full_time'), contract_on_site=Sum('contract_on_site'))
                caculated_value = lambda x, exclude_count: math.ceil(self.percentage * (abs(x - exclude_count)))
                data = []
                for x in self.job_types:
                    key = x.lower().replace(" ", "_")
                    obj = {
                        "name": x,
                        "value": 0,
                        "key": key
                    }
                    query_result = self.queryset.annotate(month=ExtractMonth('job_posted_date'),
                                                          year=ExtractYear('job_posted_date')).filter(
                        job_type__iexact=x, month=month_number, year=year)
                    if query_result:
                        jobs_count = query_result.aggregate(count=Sum('jobs'))['count']
                        excluded_jobs_count = qs[key] if qs else 0
                        obj.update({'value': caculated_value(jobs_count, excluded_jobs_count)})
                    data.append(obj)
                data_obj.append({
                    'month': month,
                    'data': data
                })
        except Exception as e:
            data_obj = []
        return data_obj





"""
# Generate Salary Range Graph
class ExtractNumericValue(models.Func):
    function = 'REGEXP_REPLACE'
    template = "%(function)s(%(expressions)s, '[^0-9.]', '', 'g')"
    output_field = FloatField()


def calculate_salary_per_anum(salary):
    if salary > 20000:
        return float(salary)
    elif salary > 1000:
        return float(salary) * 12
    else:
        return float(salary) * 12 * 8 * 30


salary_stats = []
tech_keywords = set(JobDetail.objects.only('tech_keywords').values_list('tech_keywords', flat=True))
fields = ['salary_max', 'salary_min', 'salary_format']
for x in tech_keywords:
    qs = JobDetail.objects.only(*fields)
    max_salary = qs.filter(salary_max__isnull=False, tech_keywords=x).exclude(salary_max='').annotate(
        numeric_amount=Cast(ExtractNumericValue('salary_max'), output_field=FloatField())
    ).aggregate(average_salary=Coalesce(Avg('numeric_amount'), Value(0, output_field=FloatField())))['average_salary']
    min_salary = qs.filter(salary_min__isnull=False, tech_keywords=x).exclude(salary_min='').annotate(
        numeric_amount=Cast(ExtractNumericValue('salary_min'), output_field=FloatField())
    ).aggregate(average_salary=Coalesce(Avg('numeric_amount'), Value(0, output_field=FloatField())))['average_salary']
    if max_salary > 0:
        salary_format = qs.first().salary_format
        if not qs.first().salary_format:
            max_salary = calculate_salary_per_anum(max_salary)
            min_salary = calculate_salary_per_anum(min_salary)
        salary_stats.append(
            {
                "tech_stack": x,
                "max": round(max_salary, 2),
                "min": round(min_salary, 2),
            }
        )


print(salary_stats)
"""