import openai
import pandas as pd
import regex as re
from dateutil import parser
from django.utils import timezone

from job_portal.utils.keywords_dic import keyword, languages, developer, regular_expressions, all_jobs_titles


# openai.api_key = env('CHATGPT_API_KEY')


class JobClassifier(object):

    def __init__(self, dataframe: pd.DataFrame):
        self.data_frame = dataframe

    def match_text_with_regex(self, text, regular_expression_list, tech_keywords_result):
        for x in regular_expression_list:
            regex, tech_stack = x['exp'], x['tech_stack']
            tech_stack = tech_stack.lower()
            if tech_stack not in tech_keywords_result:
                pattern = re.compile(pattern=regex)
                if pattern.search(text):
                    tech_keywords_result.add(tech_stack)

    def classify_job_with_languages(self, text, langugages_dict, tech_keywords_result):
        for key, value in langugages_dict.items():
            key = key.lower()
            if key not in tech_keywords_result:
                for x in value:
                    if x in text:
                        tech_keywords_result.add(key)

    def classifier_stage1(self, job_title, regular_expression_list, langugages_dict, tech_keywords_result):
        # check regular expression for job title
        self.match_text_with_regex(job_title, regular_expression_list, tech_keywords_result)
        # check job title with languages dictionary
        self.classify_job_with_languages(job_title, langugages_dict, tech_keywords_result)

    def find_job_techkeyword(self, job_title, regular_expression_list, langugages_dict, tech_keywords_result):
        # run stage 1 of the classifier
        self.classifier_stage1(job_title, regular_expression_list, langugages_dict, tech_keywords_result)
        self.job_classifier_stage2(job_title, tech_keywords_result)

    def job_classifier_stage2(self, job_title, tech_keywords_result):
        skills = {k.lower(): [i.lower() for i in v] for k, v in keyword.items()}
        for class_key, class_value in skills.items():
            class_key = class_key.lower()
            data = set(
                class_key for i in class_value if job_title == i.lower() and class_key not in tech_keywords_result)
            tech_keywords_result.update(data)

    def job_classifier_other_dev_stage(self, text):
        dev_list = map(str.lower, developer)
        for x in dev_list:
            if x in text:
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
        tech_keywords_result = set()
        job_title = job_title.strip().lower()
        job_description_lower = job_description.strip().lower()
        regular_expression_list = regular_expressions
        self.find_job_techkeyword(job_title, regular_expression_list, languages, tech_keywords_result)

        if job_description_lower:
            self.match_text_with_regex(job_description_lower, regular_expression_list, tech_keywords_result)
            self.classify_job_with_languages(job_description_lower, languages, tech_keywords_result)

        if 'go/golang' not in tech_keywords_result:
            pattern = re.compile(pattern='(^|\W)Go(\W|$)')
            if pattern.search(job_description):
                tech_keywords_result.add('go/golang')

        if not tech_keywords_result:
            r1 = self.job_classifier_other_dev_stage(job_title)
            r2 = self.job_classifier_other_dev_stage(job_description)
            return 'others dev' if 'others dev' in [r1, r2] else 'others'
        else:
            critical_keywords = set({'ui/ux', 'qa'})
            result = tech_keywords_result.difference(critical_keywords)
            tech_keywords_result = result if result else tech_keywords_result.intersection(critical_keywords)
            if 'c#' in tech_keywords_result and '.net' in tech_keywords_result:
                tech_keywords_result.remove('c#')
            return ','.join(list(tech_keywords_result))

    def classify_hour(self, job_date):
        # apply regex patterns to get the hours value
        try:
            value = None
            regex_hours = r'(?i)^((active|last|(posted (about|almost|over)))?.*\s)?([0-9]*\s?)(hours|hour|h|hr)\s*(ago)?'
            value = re.search(regex_hours, string=job_date, flags=re.IGNORECASE)
            if value and len(value.groups()) > 1:
                hours = int(re.findall(r'\d+', job_date)[0])
                return timezone.now() + timezone.timedelta(hours=-hours)
            else:
                return job_date
        except Exception as e:
            print(e, job_date)
            return job_date

    def classify_month(self, job_date):
        # apply regex patterns to get the hours value
        value = None
        regex_month = r'(?i)^([a-zA-Z]*\s)?([a-zA-Z]*\s)?(\d*\s?)(months|month)( ago)?'
        value = re.search(regex_month, string=job_date, flags=re.IGNORECASE)
        if value and len(value.groups()) > 1:
            if value.group(3):
                days = -int(value.group(3))
                today_date_time = timezone.now() + timezone.timedelta(days=days * 30)
                return today_date_time
            else:
                today_date_time = timezone.now() + timezone.timedelta(days=-30)
                return today_date_time
        else:
            return job_date

    def classify_year(self, job_date):
        value = None
        regex_month = r'(?i)^([a-zA-Z]*\s)?([a-zA-Z]*\s)?(\d*\s?)(years|year|y)( ago)?'
        value = re.search(regex_month, string=job_date, flags=re.IGNORECASE)
        if value and len(value.groups()) > 1:
            if value.group(3):
                years = -int(value.group(3))
                today_date_time = timezone.now() + timezone.timedelta(days=years * 365)
                return today_date_time
            else:
                today_date_time = timezone.now() + timezone.timedelta(days=-365)
                return today_date_time
        else:
            return job_date

    def classify_week(self, job_date):
        try:
            value = None
            regex_month = r'(?i)^([a-zA-Z]*\s)?([a-zA-Z]*\s)?(\d*\s?)(weeks|week|w)( ago)?'
            value = re.search(regex_month, string=job_date, flags=re.IGNORECASE)
            if value and len(value.groups()) > 1:
                if value.group(3):
                    weeks = -int(value.group(3))
                    today_date_time = timezone.now() + timezone.timedelta(days=weeks * 7)
                    return today_date_time
                else:
                    today_date_time = timezone.now() + timezone.timedelta(days=-7)
                    return today_date_time
            else:
                return job_date
        except Exception as e:
            print(e)
            return job_date

    def classify_day(self, job_date):
        # apply regex patterns to get the days value
        try:
            value = None
            regex_days = r'(?i)^(([a-zA-Z]*\s)?)+(\d*\s?)(days|day|d(\+)?)( ago)?'
            today_regex = r'(?i)(^|\W)(posted now|just (posted|now))(\W|$)'
            value = re.search(regex_days, string=job_date, flags=re.IGNORECASE)
            if value and len(value.groups()) > 1:
                days = -int(value.group(3))
                previous_date_time = timezone.now() + timezone.timedelta(days=days)
                return previous_date_time
            else:
                value = re.search(today_regex, string=job_date, flags=re.IGNORECASE)
                if value:
                    return timezone.now()
                elif 'yesterday' in job_date or 'today' in job_date:
                    previous_date_time = timezone.now() + timezone.timedelta(days=-1)
                    return previous_date_time
                else:
                    return job_date
        except Exception as e:
            print(e)
            return job_date

    def classify_min(self, job_date):
        value = None
        regex_min = r'(?i)^((active|last|recently|posted|reposted)?.*\s)?([0-9]+)(.*\s)?(minutes|minute|mins|min|m)\s*(ago)?'
        value = re.search(regex_min, string=job_date, flags=re.IGNORECASE)
        if value and len(value.groups()) > 1:
            minutes = -int(value.group(3))
            previous_date_time = timezone.now() + timezone.timedelta(minutes=minutes)
            return previous_date_time
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

    def classify_job_posted_date(self):
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].apply(
            lambda x: self.classify_hour(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].apply(
            lambda x: self.classify_day(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].apply(
            lambda x: self.classify_week(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].apply(
            lambda x: self.classify_month(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].apply(
            lambda x: self.classify_min(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].apply(
            lambda x: self.classify_year(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].apply(
            lambda x: self.convert_date(str(x)) if (x is not None) else None)
        self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].astype(object).where(
            self.data_frame['job_posted_date'].notnull(), timezone.now())  # for test now None #for test now None
        # self.data_frame['job_posted_date'] = self.data_frame['job_posted_date'].replace('', timezone.now()) #for test now None

    def classify(self):
        custom_columns = self.data_frame.columns.values.tolist()
        custom_columns.remove("job_source_url")
        custom_columns.remove("job_description")
        my_job_sources = self.data_frame["job_source_url"]
        job_descriptions_data = self.data_frame['job_description']
        custom_df = self.data_frame[custom_columns]
        self.data_frame = custom_df.applymap(lambda s: s.lower().strip() if type(s) == str else str(s).strip())
        self.data_frame["job_source_url"] = my_job_sources
        self.data_frame["job_description"] = job_descriptions_data

        self.data_frame['tech_keywords'] = self.data_frame.apply(
            lambda row: self.classify_job(str(row['job_title']), str(row['job_description'])) if (
                    row['job_title'] is not None) else None, axis=1)

        self.classify_job_posted_date()

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