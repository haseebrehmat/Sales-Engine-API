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
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type, \
    run_pia_proxy
from utils.helpers import saveLogs

total_jobs = 0


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# check if there is more jobs available or not
def data_exists(driver):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "btn-clear-blue"))
        )
        time.sleep(6)

        page_exists = driver.find_elements(By.CLASS_NAME, "btn-clear-blue")
        return False if len(page_exists) == 0 else True
    except Exception as e:
        print(e)
        saveLogs(e)
        return False


def find_jobs(driver, job_type, total_jobs):
    try:
        scrapped_data = []
        count = 0
        c_count = 4
        jobs = driver.find_elements(By.CLASS_NAME, "data-results-content-parent")
        links = driver.find_elements(By.CLASS_NAME, "job-listing-item")
        c_name = driver.find_elements(By.CLASS_NAME, "data-details")
        job_posted_date = driver.find_elements(
            By.CLASS_NAME, "data-results-publish-time")
        job_title = driver.find_elements(By.CLASS_NAME, "data-results-title")

        for job in jobs:
            try:
                data = []
                job.click()
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "jdp_title_header"))
                )
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "jdp-left-content"))
                )

                append_data(data, job_title[c_count].text)
                company = c_name[c_count].find_elements(By.TAG_NAME, "span")
                append_data(data, company[0].text)
                append_data(data, company[1].text)
                job_description = driver.find_element(By.CLASS_NAME, "jdp-left-content")
                append_data(data, job_description.text)
                append_data(data, links[count].get_attribute("href"))
                append_data(data, job_posted_date[count].text)
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "Careerbuilder")
                append_data(data, set_job_type(job_type))
                append_data(data, job_description.get_attribute('innerHTML'))
                scrapped_data.append(data)
                count += 1
                c_count += 1
                total_jobs += 1
            except Exception as e:
                print(e)
        print("Per Page Scrapped")
        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                        "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.CAREER_BUILDER)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(total_jobs=len(df), job_source="Career Builder", filename=filename)
        return total_jobs
    except Exception as e:
        saveLogs(e)
        return total_jobs


# find's job name
def load_jobs(driver, count):
    if not data_exists(driver):
        return False, count
    try:
        jobs = driver.find_elements(By.CLASS_NAME, "data-results-content-parent")
        if len(jobs) == count:
            return False, count

        count = len(jobs)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "btn-clear-blue"))
        )
        time.sleep(6)
        next_page = driver.find_elements(By.CLASS_NAME, "btn-clear-blue")
        if len(next_page) > 0:
            next_page[0].click()
            return True, count
        else:
            return False, count
    except Exception as e:
        return False, count


def accept_cookie(driver):
    try:
        accept = driver.find_elements(By.CLASS_NAME, "btn-clear-white-transparent")
        if len(accept) > 0:
            accept[0].click()
    except Exception as e:
        print(e)


def check_us_region(driver):
    try:
        driver.find_element(By.ID, "international")
        try:
            raise Exception('We are sorry, we do not operate in your country yet.')
        except Exception as e:
            saveLogs(e)
        return False
    except Exception as e:
        return True


def not_blocked(driver):
    try:
        blocked = driver.find_element(By.CLASS_NAME, "cf-error-overview")
        if 'Sorry, you have been blocked' in blocked.find_element(By.TAG_NAME, "h1").text:
            try:
                raise Exception('Sorry, you have been blocked')
            except Exception as e:
                saveLogs(e)
        return False
    except Exception as e:
        return True


# code starts from here
def career_builder(link, job_type):
    total_job = 0
    total_count = 0
    print("Career builder")
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        run_pia_proxy(driver, location='US Miami')
        try:
            flag = True
            request_url(driver, link)
            if not_blocked(driver):
                if check_us_region(driver):
                    accept_cookie(driver)
                    while flag:
                        flag, total_count = load_jobs(driver, total_count)
                        print("Loading...")
                    total_job = find_jobs(driver, job_type, total_job)
                    print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)

    except Exception as e:
        saveLogs(e)
        print(e)
    driver.quit()
