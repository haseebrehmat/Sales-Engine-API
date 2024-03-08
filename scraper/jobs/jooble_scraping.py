import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type

total_job = 0


def find_jobs(driver, job_type, total_job):
    scrapped_data = []
    date_time = str(datetime.now())
    count = 0
    time.sleep(3)
    alert = driver.find_elements(By.CLASS_NAME, "_8VULLY")
    if len(alert) > 0:
        try:
            driver.find_element(By.CLASS_NAME, "bLprmr").click()
        except:
            print("")
    jobs = driver.find_elements(By.TAG_NAME, "article")
    try:
        flag = True
        while(flag):

            for job in jobs:
                job.location_once_scrolled_into_view
            # this is the logic for click load more jobs button in this scraper 2 loaders are running
            time.sleep(5)
            jobs = driver.find_elements(By.TAG_NAME, "article")
            for job in jobs:
                job.location_once_scrolled_into_view
            time.sleep(5)
            jobs = driver.find_elements(By.TAG_NAME, "article")
            for job in jobs:
                job.location_once_scrolled_into_view
            time.sleep(5)
            if len(jobs) > 600:
                break
            try:
                driver.find_elements(By.CLASS_NAME, "jkit_AySJs")[1].click()
            except:
                flag = False
    except:
        print("")
    time.sleep(3)
    jobs = driver.find_elements(By.TAG_NAME, "article")
    chunk_count = 0
    for job in jobs:
        data = []
        try:
            job_title = job.find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, "a")
            job_source_url = job_title.get_attribute(
                'href')
            job_title = job_title.text
            job_description = job.find_element(By.CLASS_NAME, "PAM72f")
            section = job.find_element(By.TAG_NAME, "section")
            company_name = section.find_element(By.CLASS_NAME, "z6WlhX").text
            job_posted_date = section.find_element(By.CLASS_NAME, "Vk-5Da").text
            location = section.find_element(By.CLASS_NAME, "NTRJBV").text
            job_type = job_type
            job_source = "jooble"
            append_data(data, job_title)
            append_data(data, company_name)
            append_data(data, location)
            append_data(data, job_description.text)
            append_data(data, job_source_url)
            append_data(data, job_posted_date)
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, job_source)
            append_data(data, set_job_type(job_type))
            append_data(data, job_description.get_attribute('innerHTML'))
            total_job += 1
            scrapped_data.append(data)
            chunk_count += 1
        except Exception as e:
            print(e)
        if chunk_count >= 20:
            file_creation(scrapped_data)
            from scraper.schedulers.job_upload_scheduler import upload_jobs, remove_files
            upload_jobs('instant scraper', job_source)
            remove_files('instant scraper', job_source)
            chunk_count = 0
            scrapped_data = []
        count += 1
    file_creation(scrapped_data)
    return False, total_job

def file_creation(scrapped_data):
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.JOOBLE)

    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Jooble", filename=filename)

def append_data(data, field):
    data.append(str(field).strip("+"))


# Create your views here.
def jooble(link, job_type):
    print("Jooble")
    driver = configure_webdriver()
    try:
        total_job = 0
        driver.maximize_window()
        try:
            flag = True
            driver.get(link)
            while flag:
                flag, total_job = find_jobs(
                    driver, job_type, total_job)
                print("Fetching...")
        except Exception as e:
            print(e)
    except:
        print("Error Occurs. \n")
    driver.quit()
