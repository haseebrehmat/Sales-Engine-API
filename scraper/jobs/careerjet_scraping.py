import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
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
def find_jobs(driver, job_type, total_job):
    scrapped_data = []
    c = 0
    # time.sleep(3)
    jobs = driver.find_elements(By.CLASS_NAME, "clicky")

    for job in jobs:
        try:
            data = []
            time.sleep(1)
            job.click()
            time.sleep(1.5)

            job_title = driver.find_element(
                By.TAG_NAME, "h1")
            append_data(data, job_title.text)
            company_name = driver.find_element(
                By.CLASS_NAME, "company")
            append_data(data, company_name.text)
            detail = driver.find_element(By.CLASS_NAME, "details")
            address_span = detail.find_element(By.TAG_NAME, "li")
            address = address_span.find_element(By.TAG_NAME, "span")
            append_data(data, address.text)
            job_description = driver.find_element(
                By.CLASS_NAME, "content")
            append_data(data, job_description.text)
            append_data(data, driver.current_url)
            job_posted_date = driver.find_elements(By.CLASS_NAME, "badge-r")
            if len(job_posted_date) > 0:
                append_data(data, job_posted_date[0].text)
            else:
                append_data(data, 'Posted Today')
            append_data(data, "CareerJet")
            append_data(data, job_type)
            append_data(data, job_description.get_attribute('innerHTML'))

            scrapped_data.append(data)
            c += 1
            total_job += 1
        except Exception as e:
            msg = f"Exception in CareerJet Scraping {e}"
            saveLogs(e)

        driver.back()

    date_time = str(datetime.now())
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = f'scraper/job_data/careerjet - {date_time}.csv'
    df.to_csv(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="CareerJet", filename=filename)
    pagination = driver.find_elements(By.CLASS_NAME, "btn-primary-inverted")

    if len(pagination) == 0:
        return False, total_job
    else:
        try:
            if pagination[0].text == "Next page":
                pagination[0].click()
                return True, total_job
            elif pagination[0].text == "Previous page":
                if pagination[1].text == "Next page":
                    pagination[1].click()
                    return True, total_job
            return False, total_job
        except Exception as e:
            return False, total_job


# code starts from here
def careerjet(link, job_type):
    print("CareerJet")
    try:
        total_job = 0
        options = webdriver.ChromeOptions()  # newly added
        options.add_argument("--headless")
        options.add_argument("window-size=1200,1100")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )
        # options.headless = True  # newly added
        # with webdriver.Chrome('/home/dev/Desktop/selenium') as driver:
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options) as driver:  # modified
            driver.maximize_window()
            try:
                flag = True
                request_url(driver, link)
                driver.maximize_window()
                while flag:
                    flag, total_job = find_jobs(driver, job_type, total_job)
                    print("Fetching...")
                print(SCRAPING_ENDED)

            except Exception as e:
                saveLogs(e)
                print(LINK_ISSUE)
    except Exception as e:
        saveLogs(e)
        print(e)
