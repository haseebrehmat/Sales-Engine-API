import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type
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
    jobs = driver.find_elements(By.CLASS_NAME, "link-job-wrap")

    for job in jobs:
        try:
            data = []
            time.sleep(1)
            job.click()
            time.sleep(3)

            job_title = driver.find_element(
                By.CLASS_NAME, "jobPreview__header--title")
            append_data(data, job_title.text)
            company_name = driver.find_element(
                By.CLASS_NAME, "jobPreview__header--company")
            append_data(data, company_name.text)
            address = driver.find_element(
                By.CLASS_NAME, "jobPreview__header--location")
            append_data(data, address.text)
            job_description = driver.find_element(
                By.CLASS_NAME, "jobPreview__body--description")
            append_data(data, job_description.text)
            append_data(data, driver.current_url)
            job_posted_date = driver.find_elements(
                By.CLASS_NAME, "c-card__jobDatePosted")
            if len(job_posted_date) > 0:
                append_data(data, job_posted_date[0].text)
            else:
                append_data(data, 'Posted Today')
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "Talent")
            if 'remote' in job_type.lower():
                append_data(data, set_job_type(job_type))
            elif 'hybrid' in job_type.lower():
                append_data(data, set_job_type(job_type, 'hybrid'))
            else:
                append_data(data, set_job_type(job_type, 'onsite'))
            append_data(data, job_description.get_attribute('innerHTML'))

            scrapped_data.append(data)
            c += 1
            total_job += 1
        except Exception as e:
            msg = f"Exception in Talent Scraping {e}"

    date_time = str(datetime.now())
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.TALENT)
    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Talent", filename=filename)
    pagination = driver.find_elements(
        By.CLASS_NAME, "pagination")

    if len(pagination) == 0:
        return False, total_job
    else:
        next_page = pagination[0].find_elements(
            By.TAG_NAME, "a")
        try:
            next_page[-1].click()
            return True, total_job
        except Exception as e:
            return False, total_job


# code starts from here
def talent(link, job_type):
    print("Talent")
    driver = configure_webdriver()
    try:
        total_job = 0
        driver.maximize_window()
        try:
            flag = True
            request_url(driver, link)
            driver.maximize_window()
            while flag:
                flag, total_job = find_jobs(
                    driver, job_type, total_job)
                print("Fetching...")
            print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)

    except Exception as e:
        saveLogs(e)
        print(e)
    driver.quit()
