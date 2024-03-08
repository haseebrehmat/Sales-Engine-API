from datetime import datetime
from scraper.models.accounts import Accounts
from scraper.constants.const import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time

from scraper.models import JobSourceQuery
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type
from utils.helpers import saveLogs

total_job = 0


# calls url
def request_url(driver, url):
    driver.get(url)


# login method
def login(driver, email, password):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
    except Exception as e:
        print(e)
        saveLogs(e)
        return False

    try:
        driver.find_element(By.ID, "username").click()
        driver.find_element(By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys(email)

        driver.find_element(By.ID, "password").click()
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(password)

        driver.find_element(By.CLASS_NAME, "btn__primary--large").click()
        not_logged_in = driver.find_elements(
            By.CLASS_NAME, "form__label--error")
        if len(not_logged_in) > 0:
            return False

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "global-nav__primary-item"))
        )
        return True

    except Exception as e:
        print(e)
        saveLogs(e)
        return False


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, job_type, total_jobs, more_than_3, url=None):
    scrapped_data = []
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "jobs-search-results__list-item"))
        )
    except:
        print("waited for jobs")

    try:
        if url is not None:
            get_url = driver.current_url
            request_url(driver, get_url + str(url))
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "jobs-search-results__list-item"))
            )
    except Exception as e:
        saveLogs(e)
        return False, total_jobs

    time.sleep(2)
    if not data_exists(driver):
        return False, total_jobs

    jobs = driver.find_elements(
        By.CLASS_NAME, "jobs-search-results__list-item")

    for job in jobs:
        try:
            job.location_once_scrolled_into_view
        except Exception as e:
            print(e)

    address = driver.find_elements(By.CLASS_NAME, "artdeco-entity-lockup__caption")
    count = 0
    for job in jobs:
        try:
            data = []
            job.click()

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "jobs-description-content__text"))
            )

            job_title = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title")
            append_data(data, job_title.text)
            company_name = job.find_element(By.CLASS_NAME, "job-card-container__primary-description")
            append_data(data, company_name.text)
            append_data(data, address[count].text)
            job_description = driver.find_element(By.CLASS_NAME, "jobs-description-content__text")
            append_data(data, job_description.text)
            job_source_url = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__content--two-pane")
            url = job_source_url.find_element(By.TAG_NAME, 'a')
            append_data(data, url.get_attribute('href'))
            job_posted_date = job.find_element(By.TAG_NAME, "time")
            job_date = job_posted_date.text.split('\n')[0]
            if 'hours' in job_date:
                if int(job_date[0]) > 3:
                  more_than_3 += 1
            append_data(data, job_date)

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "job-details-jobs-unified-top-card__job-insight"))
            )

            try:
                estimated_salary = driver.find_elements(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-insight")[0].text
                if '$' in estimated_salary:
                    estimated_salary = estimated_salary.split('Full-time')[0]
                    estimated_salary = estimated_salary.split('Remote')[0]
                    try:
                        if 'yr' in estimated_salary:
                            append_data(data, "yearly")
                        elif 'hr' in estimated_salary:
                            append_data(data, "hourly")
                        else:
                            append_data(data, "N/A")
                    except:
                        append_data(data, "N/A")
                    try:
                        append_data(data, k_conversion(estimated_salary))
                    except:
                        append_data(data, 'N/A')
                    try:
                        salary_min = estimated_salary.split('$')[1]
                        salary_min = salary_min.split(' ')[0]
                        append_data(data, k_conversion(salary_min.split('-')[0]))
                    except:
                        append_data(data, 'N/A')
                    try:
                        salary_max = estimated_salary.split('$')[2]
                        append_data(data, k_conversion(salary_max.split(' ')[0]))
                    except:
                        append_data(data, 'N/A')
                else:
                    append_data(data, 'N/A')
                    append_data(data, 'N/A')
                    append_data(data, 'N/A')
                    append_data(data, 'N/A')
            except:
                append_data(data, 'N/A')
                append_data(data, 'N/A')
                append_data(data, 'N/A')
                append_data(data, 'N/A')

            append_data(data, "Linkedin")
            try:
                job_type_check = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-insight")
                if 'Contract' in job_type_check.text:
                    append_data(data, set_job_type('Contract'))
                elif 'Full-time' in job_type_check.text:
                    append_data(data, set_job_type('Full time'))
                else:
                    append_data(data, set_job_type(job_type))
            except Exception as e:
                print(e)
                append_data(data, set_job_type(job_type))
            append_data(data, job_description.get_attribute('innerHTML'))

            scrapped_data.append(data)
            total_jobs += 1
        except Exception as e:
            print(e)
            saveLogs(e)
        count += 1

    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.LINKEDIN_GROUP)
    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Linkedin", filename=filename)
    return True, total_jobs, more_than_3


# check if there is more jobs available or not
def data_exists(driver):
    try:
        page_exists = driver.find_elements(
            By.CLASS_NAME, "jobs-search-no-results-banner__image")
        return True if page_exists[0].text == '' else False
    except Exception as e:
        return True


# code starts from here
def linkedin_group(driver, link, job_type):
    print("linkedin group")
    saveLogs("linkedin_group_scraping.py")
    count = 0
    total_job = 0
    try:
        # jobs_types(driver, link, job_type, total_job)
        more_than_3 = 0
        request_url(driver, link)
        flag = True
        flag, total_job, more_than_3 = find_jobs(driver, job_type, total_job, more_than_3)
        if flag:
            count += 25

            while flag:
                if more_than_3 < 5:
                    flag, total_job, more_than_3 = find_jobs(driver, job_type, total_job, more_than_3, "&start=" + str(count))
                    count += 25
                else:
                  break
        else:
            print(NO_JOB_RESULT)
    except Exception as e:
        saveLogs(e)
        print(e)
