import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type
from utils.helpers import saveLogs

total_jobs = 0


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


def find_jobs(driver, job_type, total_jobs):
    try:
        scrapped_data = []
        time.sleep(3)
        jobs = driver.find_elements(By.CLASS_NAME, "show-job-description")
        for job in jobs:
            try:
                data = []
                try:
                    alert_check = driver.find_elements(By.CLASS_NAME, "modal-header")
                    if len(alert_check) > 0:
                        alert_check[0].find_element(By.CLASS_NAME, "dismiss").click()
                except Exception as e:
                    pass
                job.click()
                time.sleep(3)
                # WebDriverWait(driver, 30).until(
                #     EC.presence_of_element_located(
                #         (By.CLASS_NAME, "job-description-container"))
                # )
                append_data(data, job.text)
                company = driver.find_element(By.CLASS_NAME, "company")
                append_data(data, company.text)
                location = driver.find_element(By.CLASS_NAME, "location")
                append_data(data, location.text)
                job_description = driver.find_element(By.CLASS_NAME, "job-description-container")
                append_data(data, job_description.text)
                append_data(data, job.get_attribute("href"))
                job_posted_date = driver.find_element(By.CLASS_NAME, "listed-date")
                append_data(data, job_posted_date.text)
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "US Jora")
                append_data(data, set_job_type(job_type))
                append_data(data, job_description.get_attribute('innerHTML'))
                scrapped_data.append(data)
                total_jobs += 1
            except Exception as e:
                saveLogs(e)
                print(e)

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                        "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.USJORA)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(total_jobs=len(df), job_source="US Jora", filename=filename)

        try:
            next_btn = driver.find_elements(By.CLASS_NAME, "next-page-button")
            if len(next_btn) > 0:
                next_btn[0].location_once_scrolled_into_view
                next_btn[0].click()
                return True, total_jobs
            return False, total_jobs
        except Exception as e:
            saveLogs(e)
            return False, total_jobs
    except Exception as e:
        saveLogs(e)
        return False, total_jobs

# code starts from here
def us_jora(link, job_type):
    print("US Jora")
    total_job = 0
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        try:
            flag = True
            request_url(driver, link)
            while flag:
                flag, total_job = find_jobs(driver, job_type, total_job)
        except Exception as e:
            saveLogs(e)
    except Exception as e:
        saveLogs(e)
        print(e)
    driver.quit()
