import re
from django.utils import timezone
import pandas as pd
from dateutil import parser
from job_portal.models import JobDetail
from job_portal.utils.keywords_dic import keyword, languages, developer, regular_expressions, all_jobs_titles
from django.db.models import F, Value
import openai
from settings.base import env

openai.api_key = env('CHATGPT_API_KEY')


class JobClassifier(object):

    def __init__(self, dataframe: pd.DataFrame):
        self.data_frame = dataframe

    def classifier_stage1(self, job_title):
        # check regular expression
        for regex in regular_expressions:
            if re.search(regex['exp'], job_title):
                return regex['tech_stack']

        language_dict = languages
        # final_result = list()
        for key, value in language_dict.items():
            for x in value:
                if x.lower() in job_title:
                    return key
        return 'others'

    def find_job_techkeyword(self, job_title):
        # job_title = ",".join(job_title.split("/")).lower()

        # run stage 1 of the classififer
        job_title = job_title.lower()
        data = self.classifier_stage1(job_title)
        if data == "others":
            return self.job_classifier_stage2(job_title)
        return data

    def job_classifier_stage2(self, job_title):
        final_result = []
        skills = {k.lower(): [i.lower() for i in v] for k, v in keyword.items()}
        for class_key, class_value in skills.items():
            data = [class_key for i in class_value if job_title == i.lower()]
            final_result.extend(data)
        final_result = list(set(final_result))
        return final_result[0] if len(final_result) > 0 else self.job_classifier_other_dev_stage(job_title)

    def job_classifier_other_dev_stage(self, job_title):
        dev_list = map(str.lower, developer)
        for x in dev_list:
            if x in job_title:
                return "others dev"
        return "others"

    def get_job_title_for_others_dev(self, job_description):
        job_titles = all_jobs_titles
        # Flatten the nested dictionary into a list of all keywords
        all_keywords = [keyword for subdict in job_titles.values()
                        for subsubdict in subdict.values() for keyword in subsubdict]

        # Count the number of occurrences of each keyword in the job description
        keyword_counts = {title: sum(keyword in job_description for keyword in keywords)
                          for title, keywords in job_titles.items()}

        # Add the counts of all nested keywords to the corresponding top-level job titles
        for keyword in all_keywords:
            for title, subdict in job_titles.items():
                for subsubdict in subdict.values():
                    if keyword in subsubdict:
                        keyword_counts[title] += job_description.count(keyword)

        # Find the job title with the highest keyword count
        result = max(keyword_counts, key=keyword_counts.get)
        return result if keyword_counts[result] > 0 else 'others dev'

    def classify_job_with_chatgpt(self, job_description):
        job_titles = all_jobs_titles
        try:
            result = openai.Completion.create(
                engine="text-davinci-003",
                prompt=(
                    f"which is best job title for following job description selected from given list {job_titles}, if job description is {job_description}, then write answer in single word from above list"),
                max_tokens=2000,
                n=1,
                stop=None,
                temperature=0.7,
            )
            if len(result.choices) > 0:
                return result.choices[0].text.strip()
            else:
                return 'others dev'
        except Exception as e:
            return 'others dev'

    def classify_job(self, job_title, job_description):
        result = self.find_job_techkeyword(job_title)
        if result == 'others dev' and job_description:
            try:
                result = self.get_job_title_for_others_dev(job_description)
            except Exception as e:
                print('Expression', e)
        return result

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
        regex_date = r'(?i)[1-2]\d{3}-(0[1-9]|1[0-2])-(3[0-1]|[1-2]\d|0[1-9])t?\s?([0-9]\d:([0-9]\d+):([0-9]\d+)).([' \
                     r'0-9]\d+)z?'
        value = re.match(regex_date, string=job_date)
        if value and value.groups():
            datetime = parser.parse(job_date)
            return datetime

    def clean_job_type(self, job_type):
        value = None
        if job_type in ['contract', 'contractor']:
            value = 'contract'
        elif job_type in ['fulltime', 'full', 'fulltime', 'full/time', 'full-time']:
            value = 'full time'
        else:
            value = job_type
        return value

    def classify(self):
        custom_columns = self.data_frame.columns.values.tolist()
        custom_columns.remove("job_source_url")
        my_job_sources = self.data_frame["job_source_url"]
        custom_df = self.data_frame[custom_columns]
        self.data_frame = custom_df.applymap(lambda s: s.lower().strip() if type(s) == str else str(s).strip())
        self.data_frame["job_source_url"] = my_job_sources

        self.data_frame['tech_keywords'] = self.data_frame.apply(
            lambda row: self.classify_job(str(row['job_title']), str(row['job_description'])) if (
                    row['job_title'] is not None) else None, axis=1)

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
        # update jobs with new tech keywords according to job title
        self.data_frame = self.data_frame.applymap(lambda s: s.lower().strip() if type(s) == str else str(s).strip())
        self.data_frame['tech_keywords'] = self.data_frame.apply(
            lambda row: self.classify_job(str(row['job_title']), str(row['job_description'])) if (
                    row['job_title'] is not None) else None, axis=1)

    def update_job_type(self):
        self.data_frame['job_type'] = self.data_frame['job_type'].apply(
            lambda s: s.lower().strip() if type(s) == str else str(s).strip())
        self.data_frame['job_type'] = self.data_frame['job_type'].apply(
            lambda x: self.clean_job_type(str(x)) if (x is not None) else None)

    def update_job_source(self):
        self.data_frame['job_source'] = self.data_frame['job_source'].apply(
            lambda s: s.lower().strip() if type(s) == str else str(s).strip())
        self.data_frame['job_source'] = self.data_frame['job_source'].map(
            lambda s: s.lower().strip() if type(s) == str else str(s).strip())
