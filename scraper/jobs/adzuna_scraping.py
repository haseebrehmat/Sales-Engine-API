import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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
    try:
        scrapped_data = []
        date_time = str(datetime.now())
        count = 0

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gap-4"))
        )
        jobs = driver.find_elements(By.CLASS_NAME, "gap-2")

        for job in jobs:
            try:
                data = []
                job_title = job.find_element(By.CLASS_NAME, "gap-4")
                append_data(data, job_title.text)
                company_name = job.find_element(By.CLASS_NAME, "ui-company")
                append_data(data, company_name.text)
                address = job.find_element(By.CLASS_NAME, "ui-location")
                append_data(data, address.text)
                job_description = job.find_element(By.CLASS_NAME, "max-snippet-height")
                append_data(data, job_description.text)
                job_link = job_title.find_element(By.TAG_NAME, "a")
                append_data(data, job_link.get_attribute('href'))
                append_data(data, 'Today')
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "Adzuna")
                append_data(data, set_job_type(job_type))
                append_data(data, job_description.get_attribute('innerHTML'))
                count += 1
                total_job += 1
                scrapped_data.append(data)
            except Exception as e:
                print(e)

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                        "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.ADZUNA)
        df.to_excel(filename, index=False)

        ScraperLogs.objects.create(total_jobs=len(df), job_source="Adzuna", filename=filename)

        finished = "next"
        pagination = driver.find_elements(By.CLASS_NAME, "leading-10")
        pagination[-1].location_once_scrolled_into_view
        try:
            if finished in pagination[-1].text:
                next_page_link = pagination[-1].get_attribute('href')
                request_url(driver, next_page_link)
                return True, total_job
            return False, total_job
        except Exception as e:
            print(e)
            return False, total_job
    except Exception as e:
        saveLogs(e)
        return False, total_job


# code starts from here
def adzuna_scraping(link, job_type):
    total_job = 0
    print("Adzuna")
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        flag = True
        try:
            request_url(driver, link)
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
    driver.quit()
