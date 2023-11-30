from django.utils import timezone
from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.views import APIView
from collections import Counter, defaultdict
from job_portal.models import JobArchive, JobDetail
from job_portal.utils.keywords_dic import developer as others_dev
from fuzzywuzzy import fuzz

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
            lower_value, higher_value = previous_month_jobs_count, current_month_jobs_count
        else:
            over_all_jobs_alteration = "down"
            lower_value, higher_value = current_month_jobs_count, previous_month_jobs_count
        over_all_jobs_count_percentage = percentage(higher_value, lower_value) if lower_value != 0 else higher_value

        temp1 = job_detail_queryset_30_days.values('job_source').annotate(source_count=Count('job_source'))
        temp2 = job_archive_queryset_30_days.values('job_source').annotate(source_count=Count('job_source'))
        source_count_30_days = source_counts(temp1, temp2, True)
        source_count_30_days_reverse_order = sorted(source_count_30_days, key=lambda x: x['source_count'], reverse=False)

        temp3 = job_detail_queryset_60_days.values('job_source').annotate(source_count=Count('job_source'))
        temp4 = job_archive_queryset_60_days.values('job_source').annotate(source_count=Count('job_source'))
        source_count_60_days = source_counts(temp3, temp4, True)
        previous_2_months_count_difference = source_counts(source_count_30_days,source_count_60_days, False)
        # Here is a logic of thriving_source using previous_2_months_count_difference
        previous_2_months_source_counts_percentage = percentage_of_counts(source_count_60_days, source_count_30_days, previous_2_months_count_difference, "source")
        positive_source_count_percentage, negative_source_count_percentage = positive_negative_percentage_lists(previous_2_months_source_counts_percentage)
        positive_source_count_percentage = sorted(positive_source_count_percentage, key=lambda x: x['percentage'], reverse=True)
        negative_source_count_percentage = sorted(negative_source_count_percentage, key=lambda x: x['percentage'], reverse=True)
        if len(positive_source_count_percentage) == 0:
            source_percentage_array_positive = percentage_of_counts(source_count_60_days, source_count_30_days, source_count_30_days, "source")
        if len(negative_source_count_percentage) == 0:
            source_percentage_array_negative = percentage_of_counts(source_count_60_days, source_count_30_days, source_count_30_days_reverse_order, "source")




        # Get array of current month jobs's tech stacks
        tech_keywords_60_days = [word for job in queryset_60_days for word in job.tech_keywords.split(",")]
        tech_keywords_30_days = [word for job in queryset_30_days for word in job.tech_keywords.split(",")]
        # Get count of each tech stack and set all the tech stacks descending order
        element_counts_60_days = Counter(tech_keywords_60_days)
        element_counts_30_days = Counter(tech_keywords_30_days)


        ai_ml_count_30_days = combined_count(element_counts_30_days)
        ai_ml_count_60_days = combined_count(element_counts_60_days)
        element_counts_60_days = remove_tech_stacks(element_counts_60_days)
        element_counts_30_days = remove_tech_stacks(element_counts_30_days)


        tech_stack_counts_60_days = [{"job_source": element, "source_count": count} for element, count in element_counts_60_days.items()]

        tech_stack_counts_30_days = [{"job_source": element, "source_count": count} for element, count in
                                     element_counts_30_days.items()]
        add_tech_stack(tech_stack_counts_60_days, ai_ml_count_60_days)
        add_tech_stack(tech_stack_counts_30_days, ai_ml_count_30_days)

        tech_stack_counts_60_days = sorted(tech_stack_counts_60_days, key=lambda x: x['source_count'], reverse=True)
        tech_stack_counts_30_days = sorted(tech_stack_counts_30_days, key=lambda x: x['source_count'], reverse=True)

        tech_stack_counts_30_days_reverse_order = sorted(tech_stack_counts_30_days, key=lambda x: x['source_count'], reverse=False)

        combined_tech_stacks_difference = source_counts(tech_stack_counts_30_days, tech_stack_counts_60_days,False)

        previous_2_months_tech_stacks_percentage = percentage_of_counts(tech_stack_counts_60_days, tech_stack_counts_30_days, combined_tech_stacks_difference, "stack")

        positive_tech_stack_count_percentage, negative_tech_stack_count_percentage = positive_negative_percentage_lists(previous_2_months_tech_stacks_percentage)
        positive_tech_stack_count_percentage = sorted(positive_tech_stack_count_percentage, key=lambda x: x['percentage'],
                                                  reverse=True)
        negative_tech_stack_count_percentage = sorted(negative_tech_stack_count_percentage, key=lambda x: x['percentage'],
                                                  reverse=True)
        if len(positive_tech_stack_count_percentage) == 0:
            tech_stack_percentage_array_positive = percentage_of_counts(tech_stack_counts_60_days, tech_stack_counts_30_days, tech_stack_counts_30_days, "stack")
        if len(negative_tech_stack_count_percentage) == 0:
            tech_stack_percentage_array_negative = percentage_of_counts(tech_stack_counts_60_days, tech_stack_counts_30_days, tech_stack_counts_30_days_reverse_order, "stack")


        remove_others_dev = ["others dev", "others"]
        remove_others_queryset_60_days = [job for job in queryset_60_days if not any(keyword in job.tech_keywords for keyword in remove_others_dev)]
        remove_others_queryset_30_days = [job for job in queryset_30_days if
                                          not any(keyword in job.tech_keywords for keyword in remove_others_dev)]

        over_all_jobs_titles = [job.job_title for job in remove_others_queryset_30_days]
        job_titles_last_60_days = [job.job_title for job in remove_others_queryset_60_days]
        for job_title in job_titles_last_60_days:
            over_all_jobs_titles.append(job_title)
        emerging_titles = Counter(over_all_jobs_titles)
        emerging_titles = [{"title": element, "count": count} for element, count in emerging_titles.items()]

        emerging_titles = sorted(emerging_titles, key=lambda x: x['count'], reverse=True)
        # remove others dev from emerging titles
        emerging_titles = remove_specific_titles(emerging_titles)

        data["jobs"] = {"month": {
            "current_count": current_month_jobs_count,
            "previous_count": previous_month_jobs_count,
            "percentage": over_all_jobs_count_percentage,
            "alteration": over_all_jobs_alteration
        }, "week": {}}
        data["thriving_source_status"] = bool(positive_source_count_percentage)
        data["thriving_sources"] = {"month": positive_source_count_percentage[:5] if positive_source_count_percentage else source_percentage_array_positive[:5], "week": []}
        data["declining_source_status"] = bool(negative_source_count_percentage)
        data["declining_sources"] = {"month": negative_source_count_percentage[:5] if negative_source_count_percentage else  source_percentage_array_negative[:5], "week": []}
        data["thriving_tech_stack_status"] = bool(positive_tech_stack_count_percentage)
        data["thriving_tech_stacks"] = {"month": positive_tech_stack_count_percentage[:5] if positive_tech_stack_count_percentage else tech_stack_percentage_array_positive[:5], "week": []}
        data["declining_tech_stack_status"] = bool(negative_tech_stack_count_percentage)
        data["declining_tech_stacks"] = {"month": negative_tech_stack_count_percentage[:5] if negative_tech_stack_count_percentage else tech_stack_percentage_array_negative[:5], "week": []}
        data["thriving_titles"] = {"month": emerging_titles[:5], "week": []}
        data["emerging_titles"] = {"month": top_five_emerging_titles(job_sources, last_60_days), "week": []}
        return Response(data)
def source_counts(queryset1, queryset2, flag):
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

def percentage_of_counts(list1, list2, final_list, text):
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
            dict[text] = source
            source_percentage.append(dict)
            continue
        elif count_this_month == 0:
            dict['percentage'] = count_previous_month
            dict['alteration'] = alteration
            dict['current_count'] = count_this_month
            dict['previous_count'] = count_previous_month
            dict[text] = source
            source_percentage.append(dict)
            continue
        if count_previous_month >= count_this_month:
            per = percentage(count_previous_month, count_this_month)
        else:
            per = percentage(count_this_month, count_previous_month)
        dict['percentage'] = per
        dict['alteration'] = alteration
        dict['current_count'] = count_this_month
        dict['previous_count'] = count_previous_month
        dict[text] = source
        source_percentage.append(dict)
    return source_percentage


def percentage(max_value, min_value):
    return ((max_value - min_value) / min_value) * 100
def positive_negative_percentage_lists(percentage_list):
    positive_percentage = [x for x in percentage_list if x["alteration"] == "up"]
    negative_percentage = [x for x in percentage_list if x["alteration"] == "down"]
    return positive_percentage, negative_percentage
def remove_tech_stacks(data):
    keys_to_remove = ['others', 'others dev', 'ai/ml engineer', 'ml engineer', 'ai engineer']
    # Remove the specified keys from the Counter dictionary
    for key in keys_to_remove:
        data.pop(key, None)
    return data
def combined_count(element_counts):
    combined_stacks = ['ai/ml engineer', 'ml engineer', 'ai engineer']
    combined_count = 0
    for element, count in element_counts.items():
        if element in combined_stacks:
            combined_count = combined_count + count
    return combined_count
def add_tech_stack(array ,count):
    new_dict = {'job_source': 'ai/ml engineer', 'source_count': count}
    array.append(new_dict)
def remove_specific_titles(titles_list):
    filtered_data_list = [data_dict for data_dict in titles_list if
                          not any(keyword.lower() in data_dict['title'].lower() for keyword in others_dev)]

    return filtered_data_list


def check_similar(title1: str, title2: str) -> bool:
    similarity_threshold: float = 0.6
    matcher: float | int = fuzz.ratio(title1, title2)
    similarity: float = matcher / 100.0
    return similarity > similarity_threshold


def top_five_emerging_titles(job_sources, last_month):
    job_detail_titles = list(JobDetail.objects.only('job_title', 'tech_stacks', 'job_sources')
                             .filter(tech_stacks__contained_by=['others'], job_source__in=job_sources)
                             .values_list('job_title', flat=True))
    job_archive_titles = list(JobArchive.objects.only('job_title', 'tech_keywords', 'job_sources', 'created_at')
                              .filter(created_at__gte=last_month, tech_keywords__icontains='others', job_source__in=job_sources)
                              .values_list('job_title', flat=True))
    titles: list[str] = job_detail_titles + job_archive_titles
    title_counts: dict = defaultdict(int)
    i: int = 0
    while i < len(titles):
        title1: str = titles[i]
        j: int = i + 1
        while j < len(titles):
            title2: str = titles[j]
            if check_similar(title1, title2):
                title_counts[title1] += 1
                titles.pop(j)
            j += 1
        i += 1
    sorted_job_titles: dict = dict(sorted(title_counts.items(), key=lambda item: item[1], reverse=True))
    top_5_titles: list = [{"title": k, "count": v} for k, v in list(sorted_job_titles.items())[:5]]
    return top_5_titles

