from datetime import datetime

from job_scraper.constants.const import *
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time

from job_scraper.models import JobSourceQuery
from job_scraper.models.scraper_logs import ScraperLogs
total_job = 0

def append_data(data, field):
    data.append(str(field).strip("+"))


def load_jobs(driver):
    finished = "No More Results"
    try:
        button = driver.find_element(
            By.CLASS_NAME, "job-search-resultsstyle__LoadMoreContainer-sc-1wpt60k-1")
        data_exists = button.find_element(By.TAG_NAME, "span")
        if finished in data_exists.text:
            return False
        return True
    except:
        return False


# find's job name
def find_jobs(driver, scrapped_data, job_type):
    count = 0
    global total_job
    time.sleep(7)
    while load_jobs(driver):
        jobs = driver.find_elements(
            By.CLASS_NAME, "job-search-resultsstyle__JobCardWrap-sc-1wpt60k-5")
        for job in jobs:
            job.click()
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "descriptionstyles__DescriptionContainer-sc-13ve12b-0"))
            )
    jobs = driver.find_elements(
        By.CLASS_NAME, "job-search-resultsstyle__JobCardWrap-sc-1wpt60k-5")
    for job in jobs:
        data = []
        job.click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "descriptionstyles__DescriptionContainer-sc-13ve12b-0"))
        )
        job_title = driver.find_element(
            By.CLASS_NAME, "headerstyle__JobViewHeaderTitle-sc-1ijq9nh-5")
        append_data(data, job_title.text)
        company_name = driver.find_element(
            By.CLASS_NAME, "headerstyle__JobViewHeaderCompany-sc-1ijq9nh-6")
        append_data(data, company_name.text)
        address = driver.find_element(
            By.CLASS_NAME, "headerstyle__JobViewHeaderLocation-sc-1ijq9nh-4")
        append_data(data, address.text)
        job_description = driver.find_element(
            By.CLASS_NAME, "descriptionstyles__DescriptionBody-sc-13ve12b-4")
        append_data(data, job_description.text)
        url = driver.find_elements(
            By.CLASS_NAME, "job-cardstyle__JobCardTitle-sc-1mbmxes-2")
        append_data(data, url[count].get_attribute('href'))
        job_posted_date = driver.find_element(
            By.CLASS_NAME, "detailsstyles__DetailsTableDetailPostedBody-sc-1deoovj-6")
        append_data(data, job_posted_date.text)
        append_data(data, "Monster")
        append_data(data, job_type)
        scrapped_data.append(data)
        count += 1
        total_job += 1
    date_time = str(datetime.now())
    columns_name = ["job_title", "company_name", "address", "job_description",
                    'job_source_url', "job_posted_date", "job_source", "job_type"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    df.to_csv(f'job_scraper/job_data/monster - {date_time}.csv', index=False)


# code starts from here
def monster():
    options = webdriver.ChromeOptions()  # newly added
    options.add_argument("--headless")
    options.add_argument("window-size=1200,1100")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    )
    # options.headless = True  # newly added
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                          options=options) as driver:  # modified
        scrapped_data = []
        count = 0

        # types = [MONSTER_CONTRACT_RESULTS, MONSTER_FULL_RESULTS, MONSTER_REMOTE_RESULTS]
        types = []
        job_type = []
        for c in range(3):
            query = list(JobSourceQuery.objects.filter(job_source='monster').values_list("queries", flat=True))[0]
            types.append(query[c]['link'])
            job_type.append(query[c]['job_type'])
        for url in types:
            driver.get(url)
            driver.maximize_window()
            find_jobs(driver, scrapped_data, job_type[count])
            count += 1
    print("SCRAPING_ENDED")
    ScraperLogs.objects.create(total_jobs=total_job, job_source="Monster")


# monster()
