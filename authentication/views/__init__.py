# import pandas as pd

# from job_portal.models import JobArchive
# tech_stacks = ["python", "ai/ml", "data science/data scientist", "ml engineer", "data engineering/data engineer"]
# qs = JobArchive.objects.filter(tech_keywords__in=tech_stacks).exclude(job_description="nan").exclude(job_title="nan")
# data = [
#         {
#             "job_title": x.job_title,
#             "job_description": x.job_description,
#         } for x in qs
#     ]
# df = pd.DataFrame(
#     data
# )
#
# filename = "Job Export.xlsx"
# df.to_excel(f'authentication/{filename}', index=True)
