from fuzzywuzzy import fuzz

from job_portal.models import JobDetail, JobArchive
from tqdm import tqdm
from datetime import datetime

def find_similarity(title1, title2, similarity_score):
    return fuzz.ratio(title1, title2)
    # if title1 == title2:
    #     result = 100
    # else:
    #     key_set = frozenset([title1, title2])
    #     result = similarity_score.get(key_set)
    #     if not result:
    #         result = fuzz.ratio(title1, title2)
    #         similarity_score[key_set] = result
    # return result

def find_top_five_job_titles():
    start_time = datetime.now()
    result = {}
    similarity_score = {}
    titles = list(JobArchive.objects.only("job_title", "tech_keywords").filter(
        tech_keywords__in=['others', 'others dev']).values_list("job_title", flat=True))
    flag = True
    missing = range(len(titles))
    while flag and missing:
        current_missing = []
        size = len(missing)
        current_title = titles[missing[0]]
        result[current_title] = 1
        if size == 1:
            flag = False
        else:
            for j in range(1, size):
                temp_title = titles[missing[j]]
                res = find_similarity(current_title, temp_title, similarity_score)
                if res >= 60:
                    result[current_title] += 1
                else:
                    current_missing.append(missing[j])
            del missing
            missing = current_missing
        time_difference_seconds = (datetime.now() - start_time).total_seconds()
        # Calculate hours, minutes, and seconds
        hours, remainder = divmod(time_difference_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if not flag:
            print(f"Completed: 100%", end='\t\t\t')
        else:
            print(f"Completed: { 100 - len(missing) * 100 / len(titles)}%", end='\t\t\t')
        print("Time Spent: {} hours, {} minutes, and {} seconds".format(int(hours), int(minutes), int(seconds)))
    final_result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:5])
    print(final_result)
    return final_result


# result = find_top_five_job_titles()
# print(result)
