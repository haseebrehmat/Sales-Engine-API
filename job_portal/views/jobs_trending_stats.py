from django.utils import timezone
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from collections import Counter
from job_portal.models import JobArchive, JobDetail

class JobsTrendingStats(APIView):
    def get(self, request):
        data = {}
        job_sources = ['builtin', 'indeed', 'simplyhired', 'linkedin', 'weworkremotly', 'ziprecruiter', 'workable']
        last_30_days = timezone.now() + timezone.timedelta(days=-30)
        last_60_days = timezone.now() + timezone.timedelta(days=-60)

        job_portal_generic_queryset = JobDetail.objects.only('job_source', 'job_title', 'tech_keywords').filter(job_source__in=job_sources,
                                                               job_posted_date__gte=last_60_days)
        job_archive_generic_queryset = JobArchive.objects.only('job_source', 'job_title', 'tech_keywords').filter(job_source__in=job_sources,
                                                               job_posted_date__gte=last_60_days)


        job_detail_queryset_30_days = job_portal_generic_queryset.exclude(job_posted_date__lt=last_30_days)
        job_archive_queryset_30_days = job_archive_generic_queryset.exclude(job_posted_date__lt=last_30_days)
        queryset_30_days = list(job_detail_queryset_30_days) + list(job_archive_queryset_30_days)
        current_month_jobs_count = len(queryset_30_days)

        job_detail_queryset_60_days = job_portal_generic_queryset.exclude(job_posted_date__gte=last_30_days)
        job_archive_queryset_60_days = job_archive_generic_queryset.exclude(job_posted_date__gte=last_30_days)
        queryset_60_days = list(job_detail_queryset_60_days) + list(job_archive_queryset_60_days)
        previous_month_jobs_count = len(queryset_60_days)

        if previous_month_jobs_count <= current_month_jobs_count:
            over_all_jobs_alteration = "up"
            lower_value = previous_month_jobs_count
            higher_value = current_month_jobs_count
        else:
            over_all_jobs_alteration = "down"
            lower_value = current_month_jobs_count
            higher_value = previous_month_jobs_count
        if lower_value != 0:
            over_all_jobs_count_percentage = ((higher_value - lower_value) / lower_value) * 100
        else:
            over_all_jobs_count_percentage = higher_value


        temp1 = job_detail_queryset_30_days.values('job_source').annotate(source_count=Count('job_source'))
        temp2 = job_archive_queryset_30_days.values('job_source').annotate(source_count=Count('job_source'))
        source_count_30_days = self.source_counts(temp1, temp2, True)
        source_count_30_days_reverse_order = sorted(source_count_30_days, key=lambda x: x['source_count'], reverse=False)

        temp3 = job_detail_queryset_60_days.values('job_source').annotate(source_count=Count('job_source'))
        temp4 = job_archive_queryset_60_days.values('job_source').annotate(source_count=Count('job_source'))
        source_count_60_days = self.source_counts(temp3, temp4, True)
        previous_2_months_count_difference = self.source_counts(source_count_30_days,source_count_60_days, False)
        # Here is a logic of thriving_source using previous_2_months_count_difference
        previous_2_months_source_counts_percentage = self.percentage_of_counts(source_count_60_days, source_count_30_days, previous_2_months_count_difference)

        positive_source_count_percentage = []
        negative_source_count_percentage = []
        for x in previous_2_months_source_counts_percentage:
            if x["alteration"] == "up":
                positive_source_count_percentage.append(x)
            else:
                negative_source_count_percentage.append(x)

        positive_source_count_percentage = sorted(positive_source_count_percentage, key=lambda x: x['percentage'], reverse=True)
        negative_source_count_percentage = sorted(negative_source_count_percentage, key=lambda x: x['percentage'], reverse=True)




        # Get array of current month jobs's tech stacks
        tech_keywords_60_days = []
        for job in queryset_60_days:
            tech_stack_array = job.tech_keywords.split(",")
            for word in tech_stack_array:
                tech_keywords_60_days.append(word)
        # Get array of previous month jobs's tech stacks
        tech_keywords_30_days = []
        for job in queryset_30_days:
            tech_stack_array = job.tech_keywords.split(",")
            for word in tech_stack_array:
                tech_keywords_30_days.append(word)
        # Get count of each tech stack and set all the tech stacks descending order
        element_counts_60_days = Counter(tech_keywords_60_days)
        element_counts_30_days = Counter(tech_keywords_30_days)
        tech_stack_counts_60_days = [{"job_source": element, "source_count": count} for element, count in element_counts_60_days.items()]
        tech_stack_counts_30_days = [{"job_source": element, "source_count": count} for element, count in
                                     element_counts_30_days.items()]
        tech_stack_counts_60_days = sorted(tech_stack_counts_60_days, key=lambda x: x['source_count'], reverse=True)
        tech_stack_counts_30_days = sorted(tech_stack_counts_30_days, key=lambda x: x['source_count'], reverse=True)
        tech_stack_counts_30_days_reverse_order = sorted(tech_stack_counts_30_days, key=lambda x: x['source_count'], reverse=False)

        combined_tech_stacks_difference = self.source_counts(tech_stack_counts_30_days, tech_stack_counts_60_days,False)

        previous_2_months_tech_stacks_percentage = self.percentage_of_counts(tech_stack_counts_60_days, tech_stack_counts_30_days, combined_tech_stacks_difference)

        positive_tech_stack_count_percentage = []
        negative_tech_stack_count_percentage = []
        for x in previous_2_months_tech_stacks_percentage:
            if x["alteration"] == "up":
                positive_tech_stack_count_percentage.append(x)
            else:
                negative_tech_stack_count_percentage.append(x)

        positive_tech_stack_count_percentage = sorted(positive_tech_stack_count_percentage, key=lambda x: x['percentage'],
                                                  reverse=True)
        negative_tech_stack_count_percentage = sorted(negative_tech_stack_count_percentage, key=lambda x: x['percentage'],
                                                  reverse=True)


        over_all_jobs_titles = [job.job_title for job in queryset_30_days]
        job_titles_last_60_days = [job.job_title for job in queryset_60_days]
        for job_title in job_titles_last_60_days:
            over_all_jobs_titles.append(job_title)
        emerging_titles = Counter(over_all_jobs_titles)
        emerging_titles = [{"job_title": element, "count": count} for element, count in emerging_titles.items()]
        emerging_titles = sorted(emerging_titles, key=lambda x: x['count'], reverse=True)

        data["jobs"] = {"month":
                            {"current_count":current_month_jobs_count, "previous_count":previous_month_jobs_count,
                             "percentage":over_all_jobs_count_percentage, "alteration":over_all_jobs_alteration},
                        "week":{}}
        data["thriving_source_status"] = True if len(positive_source_count_percentage) > 0 else False
        data["thriving_sources"] = {"month":
                                        [{"source":x["source"], "current_count":x["current_count"],
                                          "previous_count":x["previous_count"],"percentage":x["percentage"],
                                          "alteration":x["alteration"]} for x in positive_source_count_percentage[:5]] if len(positive_source_count_percentage) > 0 else [{"source": x["job_source"], "current_count": x["source_count"],
                                          "previous_count": 0, "percentage": 0,
                                          "alteration": "N/A"} for x in source_count_30_days[:5]]
                                    ,
                                    "week":[]}
        data["declining_source_status"] = True if len(negative_source_count_percentage) > 0 else False
        data["declining_sources"] = {"month":
                                        [{"source": x["source"], "current_count": x["current_count"],
                                          "previous_count": x["previous_count"], "percentage": x["percentage"],
                                          "alteration": x["alteration"]} for x in
                                         negative_source_count_percentage[:5]] if len(
                                            negative_source_count_percentage) > 0 else [
                                            {"source": x["job_source"], "current_count": x["source_count"],
                                             "previous_count": 0, "percentage": 0,
                                             "alteration": "N/A"} for x in source_count_30_days_reverse_order[:5]]
            ,
                                    "week": []}

        data["thriving_tech_stack_status"] = True if len(positive_tech_stack_count_percentage) > 0 else False
        data["thriving_tech_stacks"] = {"month":
                                        [{"stack": x["source"], "current_count": x["current_count"],
                                          "previous_count": x["previous_count"], "percentage": x["percentage"],
                                          "alteration": x["alteration"]} for x in
                                         positive_tech_stack_count_percentage[:5]] if len(
                                            positive_tech_stack_count_percentage) > 0 else [
                                            {"stack": x["job_source"], "current_count": x["source_count"],
                                             "previous_count": 0, "percentage": 0,
                                             "alteration": "N/A"} for x in tech_stack_counts_30_days[:5]]
            ,
                                    "week": []}
        data["declining_tech_stack_status"] = True if len(negative_tech_stack_count_percentage) > 0 else False
        data["declining_tech_stacks"] = {"month":
                                         [{"stack": x["source"], "current_count": x["current_count"],
                                           "previous_count": x["previous_count"], "percentage": x["percentage"],
                                           "alteration": x["alteration"]} for x in
                                          negative_tech_stack_count_percentage[:5]] if len(
                                             negative_tech_stack_count_percentage) > 0 else [
                                             {"stack": x["job_source"], "current_count": x["source_count"],
                                              "previous_count": 0, "percentage": 0,
                                              "alteration": "N/A"} for x in tech_stack_counts_30_days_reverse_order[:5]]
            ,
                                     "week": []}
        data["thriving_titles"] = {"month": [{"title":x["job_title"], "count":x["count"]}
                                             for x in emerging_titles[:5]],
                                   "week": []}
        return Response(data)
    def source_counts(self, queryset1, queryset2, flag):
        if flag:
            queryset1_list = list(queryset1)
            queryset2_list = list(queryset2)
        else:
            queryset1_list = queryset1
            queryset2_list = queryset2

        # Create a dictionary to store the source counts
        source_counts = {}

        # Iterate over the first queryset and add the counts to the dictionary
        for entry in queryset1_list:
            source = entry['job_source']
            count = entry['source_count']
            if flag:
                source_counts[source] = source_counts.get(source, 0) + count
            else:
                source_counts[source] = count

        # Iterate over the second queryset and add the counts to the dictionary
        for entry in queryset2_list:
            source = entry['job_source']
            count = entry['source_count']
            if flag:
                source_counts[source] = source_counts.get(source, 0) + count
            else:
                source_counts[source] = source_counts.get(source, 0) - count

        # Convert the dictionary to a list of dictionaries
        result = [{'job_source': source, 'source_count': count} for source, count in source_counts.items()]

        # If you want to sort the result by 'source_count' in descending order:
        result = sorted(result, key=lambda x: x['source_count'], reverse=True)

        # Print the consolidated result
        return result

    def percentage_of_counts(self, list1, list2, final_list):
        source_percentage = []
        for x in final_list:
            source = x['job_source']
            count_previous_month = next((entry['source_count'] for entry in list1 if entry.get('job_source') == source), 0)
            count_this_month = next((entry['source_count'] for entry in list2 if entry.get('job_source') == source), 0)
            dict = {}
            if count_previous_month >= count_this_month:
                alteration = "down"
            else:
                alteration = "up"
            if count_previous_month == 0:
                dict['percentage'] = count_this_month
                dict['alteration'] = alteration
                dict['current_count'] = count_this_month
                dict['previous_count'] = count_previous_month
                dict['source'] = source
                source_percentage.append(dict)
                continue
            elif count_this_month == 0:
                dict['percentage'] = count_previous_month
                dict['alteration'] = alteration
                dict['current_count'] = count_this_month
                dict['previous_count'] = count_previous_month
                dict['source'] = source
                source_percentage.append(dict)
                continue
            if count_previous_month >= count_this_month:
                per = self.percentage(count_previous_month, count_this_month)
            else:
                per = self.percentage(count_this_month, count_previous_month)
            dict['percentage'] = per
            dict['alteration'] = alteration
            dict['current_count'] = count_this_month
            dict['previous_count'] = count_previous_month
            dict['source'] = source
            source_percentage.append(dict)
        return source_percentage


    def percentage(self, max_value, min_value):
        return ((max_value - min_value) / min_value) * 100




