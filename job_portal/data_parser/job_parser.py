import os

import numpy as np
import pandas as pd


class JobParser(object):
    def __init__(self, filelist):
        self.filelist = filelist
        self.job_desc_cols = ['job_title', 'company_name', 'job_source', 'job_type', 'address', 'job_description',
                              'job_posted_date', 'job_source_url', 'job_description_tags', 'salary_format',
                              'estimated_salary', 'salary_min', 'salary_max']
        if "scraper/job_data/" in self.filelist[0]:
            self.job_desc_cols = ['job_title', 'company_name', 'job_source', 'job_type', 'address', 'job_description',
                                  'job_posted_date', 'job_source_url', 'job_description_tags', 'salary_format',
                                  'estimated_salary', 'salary_min', 'salary_max']

    def validate_file(self):
        # file check extensions validation
        message = {}
        valid_extensions = ['.csv', '.xlsx', '.ods', 'odf', '.odt']
        ext = ""
        for file_item in self.filelist:
            if isinstance(file_item, str):
                for x in valid_extensions:
                    if x in file_item:
                        ext = x
                        break
            else:
                ext = os.path.splitext(file_item.name)[1]
            if not ext.lower() in valid_extensions:
                message = {'detail': 'Unsupported file extension'}
                return False, message
            # read and check if columns match
            if ext == ".csv":
                df = pd.read_csv(file_item, engine='c', nrows=1)
            else:
                df = pd.read_excel(file_item, nrows=1)

            try:
                file_item.file.seek(0)
            except Exception as e:
                print(e)
                file_item = open(file_item, 'r')
                file_item.seek(0)
            if not (set(self.job_desc_cols).issubset(df.columns) and len(df.columns) == len(self.job_desc_cols)):
                unsupported_cols_list = list(set(df.columns).difference(set(self.job_desc_cols)))
                message = {'detail': 'Unsupported columns exist in file: ' + ",".join(unsupported_cols_list)}
                return False, message
        return True, message

    def parse_file(self):
        data_frame = []
        for file in self.filelist:
            # Check whether file is in text format or not
            df = pd.DataFrame()
            if isinstance(file, str) or file.name.endswith(".csv"):
                if isinstance(file, str):
                    if file.endswith('xlsx'):
                        df = self.read_xlsx(file)
                    elif file.endswith(('.ods', 'odf', '.odt')):
                        df = self.read_odf(file)
                else:
                    df = pd.read_csv(file, engine='c')
            elif file.name.endswith('xlsx'):
                df = self.read_xlsx(file)
            elif file.name.endswith(('.ods', 'odf', '.odt')):
                df = self.read_odf(file)
            data_frame.append(df)

        # concatenate and slice only first 7 columns
        self.data_frame = pd.concat(data_frame, axis=0, ignore_index=True).iloc[:, :13]
        # self.data_frame = self.data_frame.where((pd.notnull(self.data_frame)), "")

    @classmethod
    def read_csv(self, file_path: str) -> pd:
        return pd.read_csv(file_path, engine='c', nrows=1)

    @classmethod
    def read_odf(self, file_path: str) -> pd:
        return pd.read_excel(file_path, engine='odf', nrows=1)

    @classmethod
    def read_xlsx(self, file_path: str) -> pd:
        return pd.read_excel(file_path).replace(np.nan, '', regex=True)
