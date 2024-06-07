import time

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from scraper.constants.const import *
from scraper.models.accounts import Accounts
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, previous_jobs, \
    set_job_type, run_pia_proxy
from utils.helpers import saveLogs, log_scraper_running_time
from random import randint

def login(driver, email, password):
    try:
        time.sleep(2)
        driver.find_element(By.ID, "inlineUserEmail").click()
        driver.find_element(By.ID, "inlineUserEmail").clear()
        driver.find_element(By.ID, "inlineUserEmail").send_keys(email)
        btn = driver.find_element(By.CLASS_NAME, "emailButton")
        btn.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        driver.find_element(By.ID, "inlineUserPassword").click()
        driver.find_element(By.ID, "inlineUserPassword").clear()
        driver.find_element(By.ID, "inlineUserPassword").send_keys(password)
        btn = driver.find_element(By.CLASS_NAME, "emailButton")
        btn.find_element(By.TAG_NAME, "button").click()
        time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[name='submit']")))
            return True
        except Exception as e:
            return True
    except Exception as e:
        return False


def find_jobs(driver, job_type):
    scrapped_data = []
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "salary_format", "estimated_salary", "salary_min", "salary_max", "job_source", "job_type",
                    "job_description_tags"]
    time.sleep(3)
    try:
        jobs = driver.find_elements(By.CLASS_NAME, "JobCard_jobCardContainer___hKKI")
        total_jobs = len(jobs)
        count = 0
        batch_size = 50
        try:
            close_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "modal_closeIcon")))
            close_button.click()
        except:
            pass

        job_urls = [job.find_element(By.CLASS_NAME, "JobCard_jobTitle___7I6y").get_attribute('href') for job in jobs]
        existing_jobs_dictionary = previous_jobs("glassdoor", job_urls)

        for job in jobs:
            try:
                if existing_jobs_dictionary.get(job):
                    continue
                job, error = get_job_detail(driver, job, job_type)
                if not error:
                    data = [job[c] for c in columns_name]
                    scrapped_data.append(data)
                count += 1

                # upload jobs in chunks of 50 size
                if scrapped_data and count > 0 and (count % batch_size == 0 or count == total_jobs - 1):
                    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
                    filename = generate_scraper_filename(
                        ScraperNaming.GLASSDOOR)
                    df.to_excel(filename, index=False)
                    ScraperLogs.objects.create(total_jobs=len(
                        df), job_source='Glassdoor', filename=filename)
                    scrapped_data = []
            except Exception as e:
                saveLogs(e)
    except Exception as e:
        saveLogs(e)


def get_job_detail(driver, jobs, job_type):
    try:
        jobs.click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "JobDetails_jobDescription__uW_fK"))
        )
        time.sleep(randint(1, 3))
        job_detail = jobs.text.split('\n')
        job_title = jobs.find_element(By.CLASS_NAME, "JobCard_jobTitle___7I6y")
        company_name = jobs.find_element(By.CLASS_NAME, "EmployerProfile_compactEmployerName__LE242").text.split('\n')[0]
        address = jobs.find_element(By.CLASS_NAME, "JobCard_location__rCz3x").text

        job_url = job_title.get_attribute('href')
        # click show more details for description
        try:
            driver.find_element(By.CLASS_NAME, "JobDetails_showMoreWrapper__ja2_y").click()
            time.sleep(0.5)
        except:
            pass
        job_description = driver.find_element(By.CLASS_NAME, "JobDetails_jobDescription__uW_fK")

        try:
            job_posted_date = job_detail[-1]
        except:
            job_posted_date = "24h"

        job = {
            "job_title": job_title.text,
            "company_name": company_name,
            "address": address,
            "job_description": job_description.text,
            "job_source_url": job_url,
            "job_posted_date": job_posted_date,
            "salary_format": "N/A",
            "estimated_salary": "N/A",
            "salary_min": "N/A",
            "salary_max": "N/A",
            "job_source": "Glassdoor",
            "job_type": set_job_type(job_type, determine_job_sub_type(job_type)),
            "job_description_tags": job_description.get_attribute('innerHTML')
        }
        # find salary details
        try:
            estimated_salary = job_detail[3]
            if '$' in estimated_salary:
                es = estimated_salary.split(' (')[0]
                if 'Per' in es:
                    es_salary = es.split(" Per ")
                    salary_format = es_salary[1]
                    if 'Hour' in salary_format:
                        job["salary_format"] = "hourly"
                    elif 'Month' in salary_format:
                        job["salary_format"] = "monthly"
                    elif ('Year' or 'Annum') in salary_format:
                        job["salary_format"] = "yearly"
                else:
                    job["salary_format"] = "yearly"
                job["estimated_salary"] = k_conversion(es)
                if '-' in job["estimated_salary"]:
                    salary_range = job["estimated_salary"].split(" - ")
                    job["salary_min"] = salary_range[0].split(" Per")[0]
                    job["salary_max"] = salary_range[1].split(" Per")[0]
        except Exception as e:
            saveLogs(e)
        return job, False
    except Exception as e:
        saveLogs(e)
        return None, True

def determine_job_sub_type(type):
    sub_type = 'remote'
    if 'onsite' in type.lower() or 'on site' in type.lower():
        sub_type = 'onsite'
    if 'hybrid' in type.lower():
        sub_type = 'hybrid'
    return sub_type
    

def load_jobs(driver):
    try:
        time.sleep(10)
        load_button = driver.find_element(By.CLASS_NAME, "JobsList_buttonWrapper__ticwb")
        load_button.location_once_scrolled_into_view
        load_button.find_element(By.TAG_NAME, "button").click()
        return True
    except Exception as e:
        return False


# code starts from here
@log_scraper_running_time("Glassdoor")
def glassdoor(link, job_type):
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        run_pia_proxy(driver)
        for x in Accounts.objects.filter(source='glassdoor'):
            driver.get(GLASSDOOR_LOGIN_URL)
            logged_in = login(driver, x.email, x.password)
            if logged_in:
                break
        if logged_in:
            flag = True
            driver.get(link)
            while flag:
                flag = load_jobs(driver)
            find_jobs(driver, job_type)
    except Exception as e:
        saveLogs(e)
    driver.quit()
