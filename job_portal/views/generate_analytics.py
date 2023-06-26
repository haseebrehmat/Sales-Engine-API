from datetime import datetime, timedelta

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from job_portal.models import JobDetail


class GenerateAnalytics(APIView):
    permission_classes = (AllowAny,)
    queryset = JobDetail.objects.all()
    tech_keywords = ""
    job_types = ""
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
    ]
    hybrid_remote_enums = [
        "hybrid remote",
    ]

    def get(self, request):
        self.filter_queryset(request)
        self.tech_keywords = set(self.queryset.values_list("tech_keywords", flat=True))
        self.job_types = set(self.queryset.values_list("job_type", flat=True))

        data = {
            "tech_stack_data": self.get_tech_count_stats(),
            "job_type_data": self.get_job_type_stats()
        }

        return Response(data)

    # def get_stack_date(self):
    #     return [
    #         {
    #             "name": x,
    #             "value": self.queryset.filter(tech_keywords=x).count(),
    #         } for x in self.tech_keywords]
    #
    # def get_job_type_data(self):
    #     return [
    #         {
    #             "name": x,
    #             "value": self.queryset.filter(job_type=x).count(),
    #             "tech": self.get_tech_count(x),
    #         } for x in self.job_types]
    #
    def get_tech_count_stats(self):
        data = [
            {
                "name": x,
                "total": self.queryset.filter(tech_keywords=x).count(),
                "contract_on_site": self.queryset.filter(tech_keywords=x, job_type__in=self.contract_onsite_enums).count(),
                "contract_remote": self.queryset.filter(tech_keywords=x, job_type__in=self.contract_remote_enums).count(),
                "full_time_on_site": self.queryset.filter(tech_keywords=x, job_type__in=self.full_time_onsite_enums).count(),
                "full_time_remote": self.queryset.filter(tech_keywords=x, job_type__in=self.full_time_remote_enums).count(),
                "hybrid_on_site":  self.queryset.filter(tech_keywords=x, job_type__in=self.hybrid_onsite_enums).count(),
                "hybrid_remote": self.queryset.filter(tech_keywords=x, job_type__in=self.hybrid_remote_enums).count()
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
        filter = request.GET.get("filter", False)
        if filter:
            filter = filter.split("-")
            year = filter[0]
            if filter[-1] in ["W0" + str(x) if x < 10 else "W" + str(x) for x in range(1, 53)]:
                week = filter[-1].replace("W", "")

                str_date = str(year) + "-" + str(week) + "-" + str(1)
                start_date = datetime.strptime(str_date, "%Y-%W-%w")
                end_date = datetime.strptime(str_date, "%Y-%W-%w") + timedelta(days=8) - timedelta(seconds=1)
                print(start_date, end_date)
            self.queryset = self.queryset.filter(job_posted_date__range=[start_date, end_date])
        else:
            format_string = "%Y-%m-%d"  # Replace with the format of your date string
            start_date = self.request.GET.get("start_date", False)
            end_date = self.request.GET.get("end_date", False)
            if start_date:
                # Convert the date string into a datetime object
                start_date = datetime.strptime(start_date, format_string)
                self.queryset = self.queryset.filter(created_at__gte=start_date)
            if end_date:
                end_date = datetime.strptime(end_date, format_string) - timedelta(seconds=1)
                self.queryset = self.queryset.filter(created_at__lte=end_date)

    def get_job_type_stats(self):
        job_types = [
            {"key": "Contract on site", "value": self.contract_onsite_enums},
            {"key": "Contract remote", "value": self.contract_remote_enums},
            {"key": "Full time on site", "value": self.full_time_onsite_enums},
            {"key": "Full time remote", "value": self.full_time_remote_enums},
            {"key": "Hybrid on site", "value": self.hybrid_onsite_enums},
            {"key": "Hybrid remote", "value": self.hybrid_remote_enums}
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
