import re
from django.utils import timezone
import pandas as pd
from dateutil import parser
from job_portal.models import JobDetail
from job_portal.utils.keywords_dic import keyword, languages
from django.db.models import F, Value


class JobClassifier(object):

    def __init__(self, dataframe: pd.DataFrame):
        self.data_frame = dataframe

    @staticmethod
    def find_job_techkeyword(job_title):
        skills = {k.lower(): [i.lower() for i in v] for k, v in keyword.items()}
        
        if isinstance(job_title, str):  # Full Stack Django Developer
            job_title = ",".join(job_title.split("/")).lower()
            class_list = []
            for class_key, class_value in skills.items():
                for i in class_value:
                    if job_title == i:
                        class_list.append(class_key)

            count = 0
            for key, value in languages.items():
                count += 1
                print(count)
                data = [key for x in value if x in job_title]
                class_list.extend(data)

            final_result = list(set(class_list))
            # result_data = ",".join(final_result)
            print("Terminated")

            return final_result[0] if len(final_result) > 0 else 'others'
        else:
            return 'others'

    def classify_job(self, job_title):
        return self.find_job_techkeyword(job_title)

    def classify_hour(self, job_date):
        # apply regex patterns to get the hours value
        value = None
        regex_hours = r'(?i)^(active|posted?.*\s)?([0-9]*\s?)(hours|hour|h|hr)\s*(ago)?'
        value = re.search(regex_hours, string=job_date, flags=re.IGNORECASE)
        if value and len(value.groups()) > 1:
            today_date_time = timezone.now() + timezone.timedelta(days=-1)
            return today_date_time
        else:
            return job_date

    def classify_month(self, job_date):
        # apply regex patterns to get the hours value
        value = None
        regex_month = r'(?i)^(a?.*\s)?(month)\s*(ago)?'
        value = re.search(regex_month, string=job_date, flags=re.IGNORECASE)
        if value and len(value.groups()) > 1:
            today_date_time = timezone.now() + timezone.timedelta(days=-1)
            return today_date_time
        else:
            return job_date

    def classify_day(self, job_date):
        # apply regex patterns to get the days value
        job_date = job_date
        value = None
        regex_days_1 = r'(?i)^(active\s|posted\s)?([0-9]*\s?)(days|day|d)\s?(ago)?$'
        regex_days_2 = r'(?i)^(Today?|yesterday?)+'

        value = re.search(regex_days_1, string=job_date,
                          flags=re.IGNORECASE)
        if not value:
            value = re.search(regex_days_2, string=job_date,
                              flags=re.IGNORECASE)
        if value and len(value.groups()) > 1:
            days = -int(value.group(2))
            previous_date_time = timezone.now() + timezone.timedelta(days=days)
            return str(previous_date_time)
        elif value and value.group(1):
            previous_date_time = timezone.now() + timezone.timedelta(days=-1)
            return previous_date_time
        else:
            return job_date

    def classify_min(self, job_date):
        value = None
        regex_min_1 = r'(?i)^(active|posted?.*\s)?([0-9]*\s?)(minutes|minute|mins|min|m)\s*(ago)'
        regex_min_2 = r'(?i)(just now|Just posted?|Posted moments ago?)'
        value = re.search(regex_min_1, string=job_date, flags=re.IGNORECASE)
        if not value:
            value = re.search(regex_min_2, string=job_date,
                              flags=re.IGNORECASE)
        if value and len(value.groups()) > 1:
            days = -int(value.group(2))
            previous_date_time = timezone.now() + timezone.timedelta(days=days)
            return previous_date_time
        elif value and value.group(1):
            previous_date_time = timezone.now()
            return previous_date_time
        else:
            return job_date

    def convert_date(self, job_date):
        value = None
        regex_date = r'(?i)[1-2]\d{3}-(0[1-9]|1[0-2])-(3[0-1]|[1-2]\d|0[1-9])t?\s?([0-9]\d:([0-9]\d+):([0-9]\d+)).([0-9]\d+)z?'
        value = re.match(regex_date, string=job_date)
        if value and value.groups():
            datetime = parser.parse(job_date)
            return datetime

    def clean_job_type(self, job_type):
        value = None
        if job_type in ['contract','contractor']:
            value = 'contract'
        elif job_type in ['fulltime', 'full', 'fulltime', 'full/time', 'full-time']:
            value = 'full time'
        else:
            value = job_type
        return value
    
    def classify(self):
        self.data_frame = self.data_frame.applymap(lambda s: s.lower().strip() if type(s) == str else str(s).strip())
        self.data_frame['tech_keywords'] = self.data_frame['job_title'].apply(
            lambda x: self.classify_job(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].apply(
            lambda x: self.classify_day(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].apply(
            lambda x: self.classify_hour(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].apply(
            lambda x: self.classify_min(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].apply(
            lambda x: self.classify_month(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].apply(
            lambda x: self.convert_date(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].astype(object).where(
            self.data_frame['job_posted_date'].notnull(), timezone.now())  # for test now None #for test now None
        # self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].replace('', timezone.now()) #for test now None
        self.data_frame['job_type'] = self.data_frame['job_type'].apply(
            lambda x: self.clean_job_type(str(x)))
    

    def update_tech_stack(self):
        self.data_frame.applymap(lambda s: s.lower().strip() if type(s) == str else str(s).strip())
        self.data_frame['tech_keywords'] = self.data_frame['job_title'].apply(
            lambda x: self.classify_job(str(x)) if (x is not None) else None)
    
    def update_job_type(self):
        self.data_frame = self.data_frame.applymap(lambda s: s.lower().strip() if type(s) == str else str(s).strip())
        self.data_frame['job_type'] = self.data_frame['job_type'].apply(
            lambda x: self.clean_job_type(str(x)) if (x is not None) else None)
    
    def update_job_source(self):
        self.data_frame['job_source'] = self.data_frame['job_source'].map(lambda s: s.lower().strip() if type(s) == str else str(s).strip())