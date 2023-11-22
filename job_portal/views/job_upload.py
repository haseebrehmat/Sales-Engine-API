import datetime
from threading import Thread

import pandas as pd
from django.db import transaction
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from job_portal.classifier.job_classifier import JobClassifier
from job_portal.data_parser.job_parser import JobParser
from job_portal.exceptions import InvalidFileException
from job_portal.models import JobDetail, SalesEngineJobsStats, JobUploadLogs, JobArchive
from job_portal.serializers.job_detail import JobDataUploadSerializer
from scraper.utils.thread import start_new_thread
import requests
import json

from utils.helpers import saveLogs
from utils.sales_engine import upload_jobs_in_sales_engine, upload_jobs_in_production
from settings.base import env
from tqdm import tqdm

class JobDataUploadView(CreateAPIView):
    serializer_class = JobDataUploadSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        job_file = request.FILES.getlist('file_upload', [])
        if not job_file:
            return Response({'detail': 'Files are not selected'}, status=404)

        job_parser = JobParser(job_file)
        # validate files first
        is_valid, message = job_parser.validate_file()
        if not is_valid:
            raise InvalidFileException(detail=message)
        try:
            job_parser.parse_file()
            thread = Thread(target=self.upload_file, args=(job_parser,), )
            thread.start()
        except Exception as e:
            raise InvalidFileException(detail=str(e))
        return Response({'detail': 'data uploaded successfully'}, status=200)

    @transaction.atomic
    def upload_file(self, job_parser):
        # parse, classify and upload data to database
        if job_parser.data_frame.empty:
            raise Exception("Dataframe is empty")
        classify_data = JobClassifier(job_parser.data_frame)
        classify_data.classify()

        model_instances = [
            JobDetail(job_title=job_item.job_title, company_name=job_item.company_name, job_source=job_item.job_source,
                      job_type=job_item.job_type, address=job_item.address, job_description=job_item.job_description,
                      tech_keywords=job_item.tech_keywords.replace(" / ", "").lower(),
                      tech_stacks=list(set(job_item.tech_keywords.replace(" / ", "").lower().split(','))),
                      job_posted_date=job_item.job_posted_date, job_source_url=job_item.job_source_url) for job_item
            in classify_data.data_frame.itertuples() if
            job_item.job_source_url != "" and isinstance(job_item.job_source_url, str)]

        jobs_data = JobDetail.objects.bulk_create(model_instances, ignore_conflicts=True, batch_size=1000)
        JobUploadLogs.objects.create(jobs_count=len(jobs_data))

        if env("ENVIRONMENT") == "production":
            upload_jobs_in_sales_engine(model_instances)
        if env('ENVIRONMENT') != "production":
            upload_jobs_in_production(jobs_data, filename=None)


class JobCleanerView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request):
        try:
            job_data = JobDetail.objects.all().only('pk', 'job_title', 'tech_keywords', 'tech_stacks', 'job_description').select_related()
            self.update_data(job_data)
            return Response({'detail': f'jobs updated successfully with new tech keywords!'}, status=204)
        except Exception as e:
            return Response({'detail': 'Jobs are not updated with new tech keywords!'}, status=404)

    @start_new_thread
    def update_data(self, job_data):
        try:
            data = pd.DataFrame(list(job_data.values('pk', 'job_title', 'tech_keywords', 'tech_stacks', 'job_description')))
            classify_data = JobClassifier(data)
            classify_data.update_tech_stack()

            updated_job_details = []
            for key in classify_data.data_frame.itertuples():
                update_item = job_data.get(id=key.pk)
                if update_item.tech_keywords != key.tech_keywords.lower():
                    update_item.tech_keywords = key.tech_keywords.lower()
                    update_item.tech_stacks = key.tech_keywords.lower().split(',')
                    # append the updated user object to the list
                    updated_job_details.append(update_item)

            # update jobs in bulks in small batches
            num_records = len(updated_job_details)
            batch_size = 500
            for i in tqdm(range(0, num_records, batch_size)):
                start_index = i
                end_index = min(i + batch_size, num_records)
                user_bulk_update_list = updated_job_details[start_index:end_index]
                JobDetail.objects.bulk_update(user_bulk_update_list, ['tech_keywords', 'tech_stacks'], batch_size=500)
            return num_records
        except:
            print("")


class JobTypeCleanerView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            job_data = JobDetail.objects.all()
            thread = Thread(target=self.update_data, args=(job_data,), )
            thread.start()
            return Response({'detail': f'Jobs types updated successfully !'}, status=204)
        except Exception as e:
            return Response({'detail': 'Jobs types are not updated!'}, status=404)

    def update_data(self, job_data):
        user_bulk_update_list = []
        data = pd.DataFrame(list(job_data.values('pk', 'job_type')))
        classify_data = JobClassifier(data)
        classify_data.update_job_type()
        update_count = 0

        for key in classify_data.data_frame.itertuples():
            update_item = JobDetail.objects.get(id=key.pk)
            if update_item.job_type != key.job_type:
                update_count += 1
                update_item.job_type = key.job_type
                # append the updated user object to the list
                user_bulk_update_list.append(update_item)

        # update scores of all users in one operation
        JobDetail.objects.bulk_update(user_bulk_update_list, ['job_type'])
        return update_count


class JobSourceCleanerView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            job_data = JobDetail.objects.all()
            thread = Thread(target=self.update_data, args=(job_data,), )
            thread.start()
            return Response({'detail': f'Jobs source updated successfully !'}, status=204)
        except Exception as e:
            return Response({'detail': 'Jobs source are not updated!'}, status=404)

    def update_data(self, job_data):
        user_bulk_update_list = []
        data = pd.DataFrame(list(job_data.values('pk', 'job_source')))
        classify_data = JobClassifier(data)
        classify_data.update_job_source()
        update_count = 0

        for key in classify_data.data_frame.itertuples():
            update_item = JobDetail.objects.get(id=key.pk)
            if update_item.job_source != key.job_source:
                update_count += 1
                update_item.job_source = key.job_source
                # append the updated user object to the list
                user_bulk_update_list.append(update_item)
        # update scores of all users in one operation
        JobDetail.objects.bulk_update(user_bulk_update_list, ['job_source'])
        return update_count
