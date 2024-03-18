import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from scraper.constants.const import *
from scraper.models import ScraperLogs
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
    count = 0
    try:
        time.sleep(5)
        jobs = driver.find_elements(By.CLASS_NAME, "Qai30b")

        address = driver.find_elements(By.CLASS_NAME, "gc-job-tags__location")

        for job in jobs:
            data = []
            try:
                job.location_once_scrolled_into_view
                job.click()
            except Exception as e:
                print(e)

            time.sleep(2)
            job_title = driver.find_element(By.CLASS_NAME, "p1N2lc")
            append_data(data, job_title.text)
            company_name = driver.find_element(By.CLASS_NAME, "RP7SMd")
            append_data(data, company_name.text)
            address = driver.find_element(By.CLASS_NAME, "pwO9Dc")
            append_data(data, address.text)
            job_description_1 = driver.find_element(By.CLASS_NAME, "KwJkGe")
            job_description_2 = driver.find_element(By.CLASS_NAME, "aG5W3")
            append_data(data, job_description_1.text + job_description_2.text)
            append_data(data, job.get_attribute('href'))
            # job_posted_date = driver.find_elements(By.CLASS_NAME,"posted-date")
            append_data(data, "Today")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "Google Careers")
            append_data(data, set_job_type(job_type))
            append_data(data, job_description_1.get_attribute('innerHTML') + job_description_2.get_attribute('innerHTML'))

            count += 1
            total_job += 1
            scrapped_data.append(data)

        date_time = str(datetime.now())
        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                        "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.GOOGLE_CAREERS)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(total_jobs=len(df), job_source="GoogleCareers", filename=filename)

        cookie = driver.find_elements(By.CLASS_NAME, "gc-cookie-bar__buttons")
        if len(cookie) > 0:
            c_button = cookie[0].find_elements(
                By.CLASS_NAME, "gc-button--raised")
            c_button[0].click()

    except Exception as e:
        print(e)

    time.sleep(2)
    try:
        next_page = driver.find_element(By.CLASS_NAME, "bsEDOd")
        for next in next_page.find_elements(By.CLASS_NAME, "VfPpkd-wZVHld-gruSEe-LgbsSe"):
            if next.get_attribute("aria-label") == "Go to next page":
                next.location_once_scrolled_into_view
                next.click()
                time.sleep(5)
                return True, total_job
        return False, total_job
    except:
        return False, total_job

# code starts from here
def google_careers(links, job_type):
    print("Google Careers")
    total_job = 0
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        try:
            flag = True
            request_url(driver, links)
            driver.find_element(By.CLASS_NAME, "WpHeLc").click()
            while flag:
                flag, total_job = find_jobs(driver, job_type, total_job)
        except Exception as e:
            saveLogs(e)
    except Exception as e:
        print(e)
    driver.quit()
