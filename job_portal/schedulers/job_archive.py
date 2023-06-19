# from datetime import datetime, timedelta
#
# from django.db import transaction
#
# from job_portal.models import AppliedJobStatus, JobDetail, JobArchive
# from apscheduler.schedulers.background import BackgroundScheduler
#
# from scraper.utils.thread import start_new_thread
#
# scheduler = BackgroundScheduler()
#
#
# @start_new_thread
# @transaction.atomic
# def archive_jobs():
#     print("Archiving Jobs")
#     last_30_days = datetime.now() - timedelta(days=30)
#     job_ids = AppliedJobStatus.objects.all().values_list("job_id")
#     all_jobs = JobDetail.objects.all()
#     jobs = all_jobs.filter(created_at__lte=last_30_days).exclude(id__in=job_ids)
#     bulk_data = [JobArchive(
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
#         block=x.block,
#         is_manual=x.is_manual,
#         created_at=x.created_at,
#         updated_at=x.updated_at
#     ) for x in all_jobs]
#     JobArchive.objects.bulk_create(bulk_data, ignore_conflicts=True)
#     jobs.delete()
#     print("Terminated")


# scheduler.add_job(archive_jobs, 'interval', hours=24)


