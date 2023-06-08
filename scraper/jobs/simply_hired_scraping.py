from datetime import datetime

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
total_job = 0


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, scrapped_data, job_type, page_no, total_job):
    count = 0
    time.sleep(3)
    jobs = driver.find_elements(By.CLASS_NAME, "css-12bkbc3")

    for job in jobs:
        data = []
        try:
            job.click()
            time.sleep(5)

            job_title = driver.find_element(By.CLASS_NAME, "chakra-heading")
            append_data(data, job_title.text)
            context = driver.find_elements(By.CLASS_NAME, "css-xtodu4")
            company_name = context[0].text.split("-")
            append_data(data, company_name[0])
            address = context[1].text
            append_data(data, address)
            job_description = driver.find_element(By.CLASS_NAME, "css-cxpe4v")
            append_data(data, job_description.text)
            append_data(data, job.get_attribute('href'))
            try:
                job_posted_date = context[4].text
            except Exception as e:
                job_posted_date = 'Today'
            append_data(data, job_posted_date)
            append_data(data, "Simplyhired")
            append_data(data, job_type)
            append_data(data, job_description.get_attribute('innerHTML'))

            scrapped_data.append(data)
            count += 1
            total_job += 1

        except Exception as e:
            count += 1
            saveLogs(e)
            print(e)

    date_time = str(datetime.now())
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    df.to_csv(f'scraper/job_data/simply_hired - {date_time}.csv', index=False)

    if not data_exists(driver):
        return False, total_job

    next_page = driver.find_elements(By.CLASS_NAME, "css-1wxsdwr")
    for i in next_page:
        if int(i.text) == page_no:
            i.click()
            break

    return True, total_job


# check if there is more jobs available or not
def data_exists(driver):
    pagination = driver.find_elements(By.CLASS_NAME, "css-gxlopd")
    return False if len(pagination) == 0 else True


# code starts from here
def simply_hired(link, job_type):
    total_job = 0
    print("Simply hired")
    try:
        count = 0
        scrapped_data = []
        options = webdriver.ChromeOptions()  # newly added
        options.add_argument("--headless")
        options.add_argument("window-size=1200,1100")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )
        # options.headless = True  # newly added
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options) as driver:  # modified
            # types = [SIMPLYHIREDCONTRACT, SIMPLYHIREDFULL, SIMPLYHIREDREMOTE]
            types = [link]
            job_type = [job_type]
            try:
                flag = True
                # query = list(JobSourceQuery.objects.filter(job_source='simplyhired').values_list("queries", flat=True))[0]
                # for c in range(len(query)):
                #     types.append(query[c]['link'])
                #     job_type.append(query[c]['job_type'])
                for url in types:
                    page_no = 2
                    scrapped_data = []
                    request_url(driver, url)
                    while flag:
                        flag, total_job = find_jobs(driver, scrapped_data, job_type[count], page_no, total_job)
                        page_no += 1
                        print("Fetching...")
                    count += 1
                print(SCRAPING_ENDED)
                ScraperLogs.objects.create(
                    total_jobs=total_job, job_source="Simply Hired")
            except Exception as e:
                saveLogs(e)
                print(LINK_ISSUE)
    except Exception as e:
        saveLogs(e)
        print(e)
