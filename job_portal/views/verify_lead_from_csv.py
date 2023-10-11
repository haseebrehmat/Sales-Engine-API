import re
import pandas as pd
from tqdm import tqdm
from job_portal.models import JobDetail, JobArchive
from job_portal.utils.keywords_dic import regular_expressions, keyword


# def get_techstacks(techstacks):
#     system_stacks = set()
#     for x in techstacks:
#         if x in keyword.keys():
#             system_stacks.add(x)
#         else:
#             for i in regular_expressions:
#                 regex, tech_stack = i['exp'], i['tech_stack']
#                 pattern = re.compile(pattern=regex)
#                 if pattern.search(x):
#                     system_stacks.add(tech_stack.lower())
#
#     return list(system_stacks)
#
#
# def verify_csv_leads():
#     output_path = 'job_portal/octagon_job_found.xlsx'
#     jobs_sources = list(set(JobArchive.objects.values_list('job_source', flat=True)))
#     job_sources = {x: x.lower().replace(' ', '') for x in jobs_sources if x}
#     record_found = []
#     new_job_source = {}
#     not_found = []
#     temp = []
#     try:
#         df = pd.read_csv('job_portal/leads.csv')
#         print(len(df))
#         columns = list(df.columns)
#         for x in tqdm(df.values):
#             job_source = x[2].lower().replace(' ', '')
#             job_title = x[1].lower()
#             # try:
#             #     tech_stacks = x[15].lower().replace('and', '').split(',')
#             #     tech_stacks = get_techstacks(tech_stacks)
#             # except:
#             #     tech_stacks = []
#             data = {value: x[idx] for idx, value in enumerate(columns)}
#             if job_source in job_sources.values():
#                 qs = (JobArchive.objects.only('job_title', 'job_source')
#                       .filter(job_title__iexact=job_title,
#                               job_source__iexact=job_sources[job_source])
#                       )
#                 if qs.exists():
#                     octagon_data = qs.first()
#                     temp.append({
#                         "job_title": octagon_data.job_title,
#                         "company_name": octagon_data.company_name,
#                         "job_source": octagon_data.job_source,
#                         "job_type": octagon_data.job_type,
#                         "address": octagon_data.address,
#                         "job_description": octagon_data.job_description,
#                         "tech_keywords": octagon_data.tech_keywords,
#                         "job_posted_date": str(octagon_data.job_posted_date),
#                         "job_source_url": octagon_data.job_source_url,
#                     })
#                     record_found.append(data)
#                 else:
#                     not_found.append(data)
#
#             else:
#                 if job_source in new_job_source.keys():
#                     new_job_source[job_source] = new_job_source[job_source] + 1
#                 else:
#                     new_job_source[job_source] = 1
#                 not_found.append(data)
#
#     except Exception as e:
#         print(e)
#
#     df = pd.DataFrame(record_found)
#     df.to_excel(output_path, index=True)
#
#     df = pd.DataFrame(temp)
#     df.to_excel('job_portal/octagon_jobs.xlsx', index=True)
#
#     df = pd.DataFrame(not_found)
#     df.to_excel('job_portal/not_found_jobs.xlsx', index=True)
#
#     print(new_job_source, sum(new_job_source.values()))
#     df = pd.DataFrame([new_job_source])
#     df.to_excel('job_portal/new_job_sources.xlsx', index=True)
#
#
# # verify_csv_leads()
# unavailable_sources = {
#     'startupjobs': 115,
#     'weworkremotely': 6,
#     "company'swebsite": 52,
#     'angellist': 46,
#     'greenhouse': 2,
#     'simplify': 1,
#     'directweb': 59,
#     'workable': 57,
#     'upwork': 15,
#     'viadirectemail': 24,
#     'wellfound': 19,
#     'directwebsite': 16,
#     'linkedinchat': 16,
#     'builtin.chicago': 1,
#     'rubyonremote': 11,
#     'dynamitejobs': 1,
#     'hired': 1,
#     'remotive': 1,
#     'jobilize': 1,
#     'otta': 1,
#     'web': 1,
#     'cryptojobs': 1,
#     'diversityjobs': 1,
#     'myworkdayjobs': 1,
#     'wwr': 3,
#     'b2b': 1
# }
# print(unavailable_sources, 'total => ', sum(unavailable_sources.values()))
