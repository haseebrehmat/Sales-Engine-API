from datetime import datetime

from job_scraper.constants.const import *
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time

from job_scraper.models import JobSourceQuery
from job_scraper.models.scraper_logs import ScraperLogs

total_job = 0


def login(driver):
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "email-input").click()
    driver.find_element(By.ID, "inlineUserEmail").clear()
    driver.find_element(By.ID, "inlineUserEmail").send_keys(GLASSDOOR_USERNAME)
    driver.find_element(By.CLASS_NAME, "email-button").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "password-input").click()
    driver.find_element(By.ID, "inlineUserPassword").clear()
    driver.find_element(By.ID, "inlineUserPassword").send_keys(GLASSDOOR_PASSWORD)
    driver.find_element(By.CLASS_NAME, "css-1dqhu4c").click()
    login = driver.find_elements(By.CLASS_NAME, "iconContainer")
    if len(login) > 0:
        return False
    time.sleep(5)
    return True


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, scrapped_data, job_type):
    global total_job
    count = 0
    time.sleep(3)
    date_time = str(datetime.now())
    try:
        jobs = driver.find_elements(By.CLASS_NAME, "react-job-listing")
        company_name = driver.find_elements(By.CLASS_NAME, "css-l2wjgv")
        for job in jobs:
            data = []
            job.click()
            time.sleep(2)
            job_title = driver.find_elements(By.CLASS_NAME, "css-1vg6q84")
            if job_title:
                append_data(data, job_title[0].text)
                append_data(data, company_name[count].text)
                address = driver.find_element(By.CLASS_NAME, "css-56kyx5")
                append_data(data, address.text)
                job_description = driver.find_element(By.CLASS_NAME, "jobDescriptionContent")
                append_data(data, job_description.text)
                url = driver.find_elements(By.CLASS_NAME, "css-1rd3saf")
                append_data(data, url[count].get_attribute('href'))
                job_posted_date = driver.find_elements(By.CLASS_NAME, "css-1vfumx3")
                append_data(data, job_posted_date[count].text)
                append_data(data, "Glassdoor")
                append_data(data, job_type)
            scrapped_data.append(data)
            count += 1
            total_job += 1

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                        "job_source", "job_type"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        df.to_csv(f'job_scraper/job_data/glassdoor - {date_time}.csv', index=False)
    except Exception as e:
        print(e)

    if driver.find_element(By.CLASS_NAME, "nextButton").is_enabled():
        driver.find_element(By.CLASS_NAME, "nextButton").click()
        return True
    return False


# code starts from here
def glassdoor():
    try:
        scrapped_data = []
        count = 0
        options = webdriver.ChromeOptions()  # newly added
        options.add_argument("--headless")
        options.add_argument("window-size=1200,1100")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                            options=options) as driver:  # modified
            request_url(driver, GLASSDOOR_LOGIN_URL)
            logged_in = login(driver)
            types = []
            job_type = []
            try:
                query = list(JobSourceQuery.objects.filter(job_source='glassdoor').values_list("queries", flat=True))[0]
                for c in range(len(query)):
                    types.append(query[c]['link'])
                    job_type.append(query[c]['job_type'])
                if logged_in:
                    for url in types:
                        request_url(driver, url)
                        driver.maximize_window()
                        while find_jobs(driver, scrapped_data, job_type[count]):
                            print("Fetching...")
                        print(job_type[count], "is done")
                        count += 1
                    ScraperLogs.objects.create(total_jobs=total_job, job_source="GlassDoor")
                    print(SCRAPING_ENDED)
            except Exception as e:
                print(LINK_ISSUE)
    except Exception as e:
        print(e)
