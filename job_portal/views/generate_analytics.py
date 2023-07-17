from datetime import datetime, timedelta, date

from django.db.models.functions import ExtractMonth, ExtractYear
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from job_portal.models import JobDetail, JobArchive


class GenerateAnalytics(APIView):
    permission_classes = (AllowAny,)
    job_archive = JobArchive.objects.all()
    queryset = JobDetail.objects.all()
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
        "contract on site"
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
        "remote"
    ]
    hybrid_onsite_enums = [
        "hybrid onsite",
        "hybrid on site",
        "hybrid full time",
        "hybrid remote",
    ]
    hybrid_contract_enums = [
        "hybrid contract"
    ]

    def get(self, request):
        filters = self.filter_queryset(request)
        if self.queryset.count() == 0:
            self.queryset = self.job_archive
            filters = self.filter_queryset(request)
        self.tech_keywords = set(self.queryset.values_list("tech_keywords", flat=True))
        self.job_types = set(self.queryset.values_list("job_type", flat=True))

        data = {
            "tech_stack_data": self.get_tech_count_stats(),
            "job_type_data": self.get_job_type_stats(),
            "filters": filters,
        }

        return Response(data)

    def get_tech_count_stats(self):
        data = [
            {
                "name": x,
                "total": self.queryset.filter(tech_keywords=x).count(),
                "contract_on_site": self.queryset.filter(tech_keywords=x, job_type__in=self.contract_onsite_enums).count(),
                "contract_remote": self.queryset.filter(tech_keywords=x, job_type__in=self.contract_remote_enums).count(),
                "full_time_on_site": self.queryset.filter(tech_keywords=x, job_type__in=self.full_time_onsite_enums).count(),
                "full_time_remote": self.queryset.filter(tech_keywords=x, job_type__in=self.full_time_remote_enums).count(),
                "hybrid_full_time":  self.queryset.filter(tech_keywords=x, job_type__in=self.hybrid_onsite_enums).count(),
                "hybrid_contract": self.queryset.filter(tech_keywords=x, job_type__in=self.hybrid_contract_enums).count()
            } for x in self.tech_keywords]

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
        year_filter = request.GET.get("year", "")
        quarter_filter = request.GET.get("quarter", "")
        month_filter = request.GET.get("month", "")
        week_filter = request.GET.get("week", "")

        if week_filter != "":
            filter = week_filter.split("-")
            year = filter[0]
            if filter[-1] in ["W0" + str(x) if x < 10 else "W" + str(x) for x in range(1, 53)]:
                week = filter[-1].replace("W", "")

                str_date = str(year) + "-" + str(week) + "-" + str(1)
                start_date = datetime.strptime(str_date, "%Y-%W-%w")
                end_date = datetime.strptime(str_date, "%Y-%W-%w") + timedelta(days=8) - timedelta(seconds=1)
            self.queryset = self.queryset.filter(job_posted_date__range=[start_date, end_date])

        elif month_filter != "":
            data = month_filter.split("-")
            year = data[0]
            month = data[1]
            str_date = month_filter + "-" + str(1)
            start_date = datetime.strptime(str_date, "%Y-%M-%d")
            end_date = datetime.strptime(str_date, "%Y-%M-%d") + timedelta(days=30) - timedelta(seconds=1)
            print(start_date, end_date)
            self.queryset = self.queryset.annotate(
                month=ExtractMonth('created_at'),
                year=ExtractYear('created_at')).filter(month=month, year=year)

            data = {"weeks": self.get_week_numbers(year, month)}
            
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
                # end_date = datetime(year, quarter_number, 1) - timedelta(days=1)

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
                    for x in range(quarter_number, quarter_number+3)],
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
                end_date = datetime.strptime(end_date, format_string) - timedelta(seconds=1)
                self.queryset = self.queryset.filter(created_at__lte=end_date)

        return data

    def get_job_type_stats(self):
        job_types = [
            {"key": "Contract on site", "value": self.contract_onsite_enums},
            {"key": "Contract remote", "value": self.contract_remote_enums},
            {"key": "Full time on site", "value": self.full_time_onsite_enums},
            {"key": "Full time remote", "value": self.full_time_remote_enums},
            {"key": "Hybrid on site", "value": self.hybrid_onsite_enums},
            {"key": "Hybrid remote", "value": self.hybrid_contract_enums}
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
