from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from scraper.constants.const import *
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time

from scraper.models import JobSourceQuery
from scraper.models.scraper_logs import ScraperLogs
from utils.helpers import saveLogs

total_jobs = 0


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# check if there is more jobs available or not
def data_exists(driver):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "btn-clear-blue"))
        )
        time.sleep(6)

        page_exists = driver.find_elements(By.CLASS_NAME, "btn-clear-blue")
        return False if len(page_exists) == 0 else True
    except Exception as e:
        print(e)
        saveLogs(e)
        return False


def find_jobs(driver, scrapped_data, job_type):
    global total_jobs
    count = 0
    c_count = 4
    try:
        jobs = driver.find_elements(By.CLASS_NAME, "data-results-content-parent")
        links = driver.find_elements(By.CLASS_NAME, "job-listing-item")
        c_name = driver.find_elements(By.CLASS_NAME, "data-details")
        job_posted_date = driver.find_elements(
            By.CLASS_NAME, "data-results-publish-time")
        job_title = driver.find_elements(By.CLASS_NAME, "data-results-title")

        for job in jobs:
            try:
                data = []
                job.click()
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "jdp_title_header"))
                )
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "jdp-left-content"))
                )

                append_data(data, job_title[c_count].text)
                company = c_name[c_count].find_elements(By.TAG_NAME, "span")
                append_data(data, company[0].text)
                append_data(data, company[1].text)
                job_description = driver.find_element(
                    By.CLASS_NAME, "jdp-left-content")
                append_data(data, job_description.text)
                append_data(data, links[count].get_attribute("href"))
                append_data(data, job_posted_date[count].text)
                append_data(data, "Careerbuilder")
                append_data(data, job_type)
                scrapped_data.append(data)
                count += 1
                c_count += 1
            except Exception as e:
                print(e)
                saveLogs(e)
        print("Per Page Scrapped")
    except Exception as e:
        print(e)
    date_time = str(datetime.now())
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "job_source", "job_type"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    df.to_csv(f'scraper/job_data/career_builder - {date_time}.csv', index=False)


# find's job name
def load_jobs(driver):
    if not data_exists(driver):
        return False
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "btn-clear-blue"))
        )
        time.sleep(6)
        next_page = driver.find_elements(By.CLASS_NAME, "btn-clear-blue")
        if len(next_page) > 0:
            next_page[0].click()
            return True
        else:
            return False
    except Exception as e:
        saveLogs(e)
        return False


def accept_cookie(driver):
    accept = driver.find_elements(By.CLASS_NAME, "btn-clear-white-transparent")
    if len(accept) > 0:
        accept[0].click()


# code starts from here
def career_builder(link, job_type):
    print("Career builder")
    try:
        print("career_builder started ... ")
        count = 0
        scrapped_data = []
        options = webdriver.ChromeOptions()  # newly added
        options.add_argument("--headless")
        options.add_argument("window-size=1200,1100")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options) as driver:  # modified
            driver.maximize_window()
            # types = [CAREERBUILDER_CONTRACT_RESULTS, CAREERBUILDER_FULL_RESULTS, CAREERBUILDER_REMOTE_RESULTS]
            types = [link]
            job_type = [job_type]
            try:
                # query = list(JobSourceQuery.objects.filter(job_source='careerbuilder').values_list("queries", flat=True))[0]
                # for c in range(len(query)):
                #     types.append(query[c]['link'])
                #     job_type.append(query[c]['job_type'])
                for url in types:
                    request_url(driver, url)
                    accept_cookie(driver)
                    while load_jobs(driver):
                        print("Loading...")
                    find_jobs(driver, scrapped_data, job_type[count])
                    count += 1
                ScraperLogs.objects.create(
                    total_jobs=total_jobs, job_source="Career Builder")
                print(SCRAPING_ENDED)
            except Exception as e:
                saveLogs(e)
                print(LINK_ISSUE)
    except Exception as e:
        saveLogs(e)
        print(e)
