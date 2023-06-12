import json
import re
from datetime import datetime
from math import ceil

import numpy as np
import pandas as pd
import urllib3
from bs4 import BeautifulSoup
from scipy.stats import norm
from tqdm import tqdm

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from utils.helpers import saveLogs

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
http = urllib3.PoolManager()

results_div_index = 3


def cleanhtml(raw_html):
    try:
        return re.sub(CLEANR, '', raw_html)
    except Exception as e:
        print(e)


def ranges_of_salaries(std, mu, results):
    try:
        ppf_func = np.vectorize(norm.ppf)
        array = np.linspace(0, 1, results)
        array_z = ppf_func(array[1:-1])
        find_sample = np.vectorize(lambda z, std, mu: (z * std) + mu)
        find_sample = np.insert(find_sample(array_z, std, mu), 0, 0)
        find_sample = np.abs(find_sample.astype(int))
        return find_sample
    except Exception as e:
        print(e)


def fetch_results(soup):
    global results_div_index
    try:
        if re.search(r'results:.*\[(.|\n)*\]',
                     soup.find_all('script', {'type': "text/javascript"})[results_div_index].text):
            res = re.search(r'results:.*\[(.|\n)*\]',
                            soup.find_all('script', {'type': "text/javascript"})[results_div_index].text)
        else:
            for index, result in enumerate(soup.find_all('script', {'type': "text/javascript"})):
                if "az_wj_data" in result.text:
                    results_div_index = index
                    res = re.search(r'results:.*\[(.|\n)*\]', result.text)
        results = "{" + res.group().replace("results", "\"results\"", 1) + "}"
        return results
    except Exception as e:
        print(e)


def transform_data(df, job_type):
    try:
        df.rename(columns={'title': 'job_title', 'company': 'company_name', 'contract_type': 'job_type',
                           'location_raw': 'address', 'description': 'job_description', 'created': 'job_posted_date',
                           'numeric_id': 'job_source_url'}, inplace=True)
        count = 0
        for i in df['job_description']:
            df['job_description'][count] = cleanhtml(i)
            count += 1
        df['job_source_url'] = 'https://www.adzuna.com/details/' + \
                               df['job_source_url'].astype(str)
        df['job_title'] = df['job_title'].str.replace('<.*?>', '', regex=True)
        df['job_source'] = 'Adzuna'
        df['job_type'] = job_type
        return df
    except Exception as e:
        print(e)


def adzuna_scraping(links, job_type):
    print("Adzuna")
    try:
        r = http.request('GET', links)
        soup = BeautifulSoup(r.data, 'html.parser')
        total_results = ceil(
            int(soup.select('[data-cy-count]')[0]['data-cy-count']) / 500)
        df = pd.DataFrame()
        salary_ranges = ranges_of_salaries(
            SALARY_STD, SALARY_AVERAGE, total_results)
        for i in tqdm(range(len(salary_ranges))):
            try:
                # types = JobSourceQuery.objects.filter(job_source='adzuna').first()
                link = f'{links}&sf={salary_ranges[i]}&st={salary_ranges[i + 1]}'
            except:
                # types = JobSourceQuery.objects.filter(job_source='adzuna').first()
                link = f'{links}&sf={salary_ranges[i]}'
            r = http.request('GET', link)
            soup = BeautifulSoup(r.data, 'html.parser')
            try:
                no_of_pages = min(
                    ceil(int(soup.select('[data-cy-count]')[0]['data-cy-count']) / ADZUNA_RESULTS_PER_PAGE),
                    ADZUNA_PAGE_CAP)
            except Exception as e:
                saveLogs(e)
                continue

            per_link_data = pd.DataFrame()
            for page_number in tqdm(range(no_of_pages)):
                r = http.request('GET', f'{link}&p={page_number}')
                soup = BeautifulSoup(r.data, 'html.parser')
                results = fetch_results(soup)
                df = pd.DataFrame(json.loads(results)['results'])
                try:
                    df = df[['title', 'company', 'contract_type',
                             'location_raw', 'description', 'created', 'numeric_id']]
                except KeyError as e:
                    if 'None of' in e.args[0]:
                        continue
                    elif 'contract_type' in e.args[0]:
                        df = df[['title', 'company', 'location_raw',
                                 'description', 'created', 'numeric_id']]
                    else:
                        saveLogs(e)
                        raise e
                per_link_data = pd.concat(
                    [per_link_data, transform_data(df, job_type)], axis=0, ignore_index=True)

            df = pd.concat([df, per_link_data], axis=0, ignore_index=True)
        date_time = str(datetime.now())
        filename = f'scraper/job_data/adzuna_results - {date_time}.csv'
        df.to_csv(filename, index=False)
        ScraperLogs.objects.create(total_jobs=len(df), job_source="Adzuna", filename=filename)
    except Exception as e:
        saveLogs(e)
        print(e)
