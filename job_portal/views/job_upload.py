from threading import Thread

import pandas as pd
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from job_portal.classifier.job_classifier import JobClassifier
from job_portal.data_parser.job_parser import JobParser
from job_portal.exceptions import InvalidFileException
from job_portal.models import JobDetail
from job_portal.serializers.job_detail import JobDataUploadSerializer
from job_scraper.utils.thread import start_new_thread


class JobDataUploadView(CreateAPIView):
    serializer_class = JobDataUploadSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        job_file = request.FILES.getlist('file_upload', [])
        if not job_file:
            return Response({'detail': 'Files are not selected'},
                            status=404)

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

    def upload_file(self, job_parser):
        # parse, classify and upload data to database
        classify_data = JobClassifier(job_parser.data_frame)
        classify_data.classify()

        model_instances = [
            JobDetail(
                job_title=job_item.job_title,
                company_name=job_item.company_name,
                job_source=job_item.job_source,
                job_type=job_item.job_type,
                address=job_item.address,
                job_description=job_item.job_description,
                tech_keywords=job_item.tech_keywords.replace(" / ", "").lower(),
                job_posted_date=job_item.job_posted_date,
                job_source_url=job_item.job_source_url,
            ) for job_item in classify_data.data_frame.itertuples()
            if job_item.job_source_url != "" and isinstance(job_item.job_source_url, str)
        ]

        JobDetail.objects.bulk_create(
            model_instances, ignore_conflicts=True, batch_size=1000)


class JobCleanerView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            job_data = JobDetail.objects.all().select_related()
            # thread = Thread(target=self.update_data, args=(job_data,), )
            # thread.start()
            self.update_data(job_data)
            return Response({'detail': f'jobs updated successfully with new tech keywords!'}, status=204)
        except Exception as e:
            return Response({'detail': 'Jobs are not updated with new tech keywords!'}, status=404)

    @start_new_thread
    def update_data(self, job_data):
        print("Cleaning Jobs")
        data = pd.DataFrame(list(job_data.values('pk', 'job_title', 'tech_keywords', 'job_description')))
        classify_data = JobClassifier(data)
        classify_data.update_tech_stack()

        updated_job_details = []
        for key in classify_data.data_frame.itertuples():
            update_item = job_data.get(id=key.pk)
            if update_item.tech_keywords != key.tech_keywords.lower():
                update_item.tech_keywords = key.tech_keywords.lower()
                # append the updated user object to the list
                updated_job_details.append(update_item)

        # update jobs in bulks in small batches
        num_records = len(updated_job_details)
        batch_size = 500
        print("before bulk update")
        for i in range(0, num_records, batch_size):
            start_index = i
            end_index = min(i + batch_size, num_records)
            user_bulk_update_list = updated_job_details[start_index:end_index]
            JobDetail.objects.bulk_update(user_bulk_update_list, ['tech_keywords'])
        print('job updated successfully!')
        return num_records


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
