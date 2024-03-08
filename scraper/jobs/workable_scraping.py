from tqdm import tqdm
import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type
from utils.helpers import saveLogs

total_job = 0

# calls url


def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# loading jobs
def loading(driver, count):
    try:
        time.sleep(3)
        load = driver.find_element(
            By.CLASS_NAME, "jobsList__button-container--3FEJ-")
        btn = load.find_element(By.TAG_NAME, "button")
        btn.location_once_scrolled_into_view
        btn.click()
        count += 1
        if count == 30:
            return False, count
        return True, count
    except Exception as e:
        return False, count


# click accept cookie modal
def accept_cookie(driver):
    try:
        driver.find_element(
            By.CLASS_NAME, "styles__accept-button--1eW01").click()
    except Exception as e:
        print(e)


def find_job_link(job):
    return job.find_element(By.TAG_NAME, "a").get_attribute("href")

# find's job


def find_jobs(driver, job_type):
    try:
        scrapped_data = []
        count = 0
        time.sleep(3)
        jobs = driver.find_elements(
            By.CLASS_NAME, "jobsList__list-item--3HLIF")
        job_urls = [find_job_link(job) for job in jobs]
        print('total jobs', len(jobs))
        for url in tqdm(job_urls):
            try:
                data = []
                driver.get(url)

                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "jobBreakdown__job-breakdown--31MGR"))
                )
                job_title = driver.find_element(
                    By.CLASS_NAME, "jobOverview__job-title--kuTAQ")
                append_data(data, job_title.text)
                company_name = driver.find_element(
                    By.CLASS_NAME, "companyName__link--2ntbf")
                append_data(data, company_name.text)
                address = driver.find_elements(
                    By.CLASS_NAME, "jobDetails__job-detail--3As6F")[1]
                append_data(data, address.text)
                job_description = driver.find_element(
                    By.CLASS_NAME, "jobBreakdown__job-breakdown--31MGR")
                append_data(data, job_description.text)
                append_data(data, driver.current_url)
                job_posted_date = driver.find_element(
                    By.CLASS_NAME, "jobOverview__date-posted-container--9wC0t")
                append_data(data, job_posted_date.text)
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "Workable")
                try:
                    job_type_check = driver.find_element(
                        By.CLASS_NAME, "jobOverview__job-details--3JOit")
                    if 'contract' in job_type_check.text.lower():
                        append_data(data, set_job_type('Contract', determine_job_sub_type(job_type_check.text)))
                    elif 'full time' in job_type_check.text.lower():
                        append_data(data, set_job_type('Full time', determine_job_sub_type(job_type_check.text)))
                    else:
                        append_data(data, set_job_type(job_type))
                except Exception as e:
                    print(e)
                    append_data(data, set_job_type(job_type))
                append_data(data, job_description.get_attribute('innerHTML'))
                scrapped_data.append(data)
                count += 1
            except Exception as e:
                saveLogs(e)

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                        "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.WORKABLE)
        df.to_excel(filename, index=False)

        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="Workable", filename=filename)
        return True
    except Exception as e:
        saveLogs(e)
        return False

def determine_job_sub_type(type):
    sub_type = 'onsite'
    if 'remote' in type.lower():
        sub_type = 'remote'
    if 'hybrid' in type.lower():
        sub_type = 'hybrid'
    return sub_type
    

# code starts from here
def workable(link, job_type):
    print("Workable")
    driver = configure_webdriver(block_media=True, block_elements=['img'])
    try:
        driver.maximize_window()
        try:
            flag = True
            request_url(driver, link)
            driver.maximize_window()
            accept_cookie(driver)
            count = 0
            while flag:
                flag, count = loading(driver, count)
            if find_jobs(driver, job_type):
                print(SCRAPING_ENDED)
            else:
                print(ERROR_TEXT)
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)
    except Exception as e:
        saveLogs(e)
    driver.quit()


# workable('https://jobs.workable.com/search?query=developer&location=United%20States&remote=true', 'remote')
