import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

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


# find's job name
def find_jobs(driver, job_type, total_job):
    scrapped_data = []
    c = 0
    time.sleep(3)
    jobs = driver.find_elements(By.CLASS_NAME, "slider_container")
    company_name = driver.find_elements(By.CLASS_NAME, "companyName")
    for job in jobs:
        try:
            data = []
            time.sleep(1)
            job.click()
            time.sleep(4)

            job_title = driver.find_element(
                By.CLASS_NAME, "jobsearch-JobInfoHeader-title")
            append_data(data, job_title.text.replace('- job post', ''))
            append_data(data, company_name[c].text)
            address = driver.find_element(By.CLASS_NAME, "css-6z8o9s")
            append_data(data, address.text.replace('•Remote', ''))
            job_description = driver.find_element(
                By.CLASS_NAME, "jobsearch-jobDescriptionText")
            append_data(data, job_description.text)
            append_data(data, driver.current_url)
            job_posted_date = driver.find_elements(By.CLASS_NAME, "css-659xjq")
            if len(job_posted_date) > 0:
                append_data(data, job_posted_date[0].text)
            else:
                append_data(data, 'Posted Today')
            try:
                estimated_salary = driver.find_element(By.CLASS_NAME, "css-2iqe2o")
                a_an = ''
                if 'an' in estimated_salary.text:
                    a_an = 'an'
                else:
                    a_an = 'a'
                if 'hour' in estimated_salary.text.split(a_an)[1]:
                    append_data(data, "hourly")
                elif ('year' or 'annum') in estimated_salary.text.split(a_an)[1]:
                    append_data(data, "yearly")
                elif 'month' in estimated_salary.text.split(a_an)[1]:
                    append_data(data, "monthly")
                else:
                    append_data(data, "N/A")
                try:
                    append_data(data, k_conversion(estimated_salary.text.split(a_an)[0]))
                except:
                    append_data(data, "N/A")
                try:
                    salary_min = estimated_salary.text.split('$')[1]
                    append_data(data, k_conversion(salary_min.split(' ')[0]))
                except:
                    append_data(data, "N/A")
                try:
                    salary_max = estimated_salary.text.split('$')[2]
                    append_data(data, k_conversion(salary_max.split(' ')[0]))
                except:
                    append_data(data, "N/A")
            except:
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
            append_data(data, "Indeed")
            append_data(data, set_job_type(job_type))
            append_data(data, job_description.get_attribute('innerHTML'))

            scrapped_data.append(data)
            c += 1
            total_job += 1
        except Exception as e:
            msg = f"Exception in Indeed Scraping {e}"

    date_time = str(datetime.now())
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.INDEED)
    df.to_excel(filename, index=False)

    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Indeed", filename=filename)

    if not data_exists(driver):
        return False, total_job

    next_page = driver.find_element(
        By.CSS_SELECTOR, "a[aria-label='Next Page']")
    next_page.click()

    return True, total_job


# check if there is more jobs available or not
def data_exists(driver):
    page_exists = driver.find_elements(
        By.CSS_SELECTOR, "a[aria-label='Next Page']")
    return False if len(page_exists) == 0 else True


# code starts from here
def indeed(link, job_type):
    print("Indeed")
    try:
        total_job = 0
        count = 0
        driver = configure_webdriver()
        driver.maximize_window()
        try:
            flag = True
            request_url(driver, link)
            driver.maximize_window()
            while flag:
                flag, total_job = find_jobs(
                    driver, job_type, total_job)
                print("Fetching...")
            count += 1
            print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)

        driver.quit()
    except Exception as e:
        saveLogs(e)
        print(e)
