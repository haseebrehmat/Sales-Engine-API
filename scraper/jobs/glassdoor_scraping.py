import time

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from scraper.constants.const import *
from scraper.models.accounts import Accounts
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, \
    set_job_type, run_pia_proxy
from utils.helpers import saveLogs


def login(driver, email, password):
    try:
        time.sleep(2)
        driver.find_element(By.NAME, "username").click()
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys(
            email)
        driver.find_element(By.CSS_SELECTOR, "button.Button").click()
        time.sleep(2)
        driver.find_element(By.NAME, "password").click()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[name='submit']").click()
        time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[name='submit']")))
            return True
        except Exception as e:
            return True
    except Exception as e:
        print(e)
        return False


def find_jobs(driver, job_type):
    scrapped_data = []
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "salary_format", "estimated_salary", "salary_min", "salary_max", "job_source", "job_type",
                    "job_description_tags"]
    time.sleep(3)
    try:
        jobs = driver.find_elements(
            By.CLASS_NAME, "JobCard_jobCardContainer__l0svv")
        total_jobs = len(jobs)
        count = 0
        print(total_jobs)
        batch_size = 50
        try:
            close_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "modal_closeIcon")))
            close_button.click()
        except:
            pass
        for job in jobs:
            try:
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
                print(e)
                saveLogs(e)
    except Exception as e:
        saveLogs(e)
        print(e)


def get_job_detail(driver, jobs, job_type):
    try:
        jobs.click()
        time.sleep(3)
        job_detail = jobs.text.split('\n')
        job_title = jobs.find_element(
            By.CLASS_NAME, "JobCard_seoLink__WdqHZ").text
        company_name = jobs.find_element(
            By.CLASS_NAME, "EmployerProfile_profileContainer__d5rMb").text.split('\n')[0]
        address = jobs.find_element(
            By.CLASS_NAME, "JobCard_location__N_iYE").text

        job_url = jobs.find_element(
            By.CLASS_NAME, "JobCard_trackingLink__zUSOo").get_attribute('href')
        # click show more details for description
        try:
            driver.find_element(
                By.CLASS_NAME, "JobDetails_showMore__j5Z_h").click()
            time.sleep(0.5)
        except:
            pass
        job_description = driver.find_element(
            By.CLASS_NAME, "JobDetails_jobDescription__6VeBn")

        try:
            job_posted_date = job_detail[-1]
        except:
            job_posted_date = "24h"

        job = {
            "job_title": job_title,
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
            "job_type": set_job_type(job_type),
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
            print(e)
            saveLogs(e)
        return job, False
    except Exception as e:
        saveLogs(e)
        return None, True


def load_jobs(driver):
    try:
        time.sleep(3)
        driver.find_element(
            By.CSS_SELECTOR, "div.JobsList_wrapper__wgimi > div > button").click()
        return True
    except Exception as e:
        return False

# code starts from here


def glassdoor(link, job_type):
    print("Glassdoor")
    try:
        driver = configure_webdriver()
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
            pre = driver.find_elements(
                By.CLASS_NAME, 'JobCard_jobCardContainer__l0svv')
            while flag:

                flag = load_jobs(driver)
                next = driver.find_elements(
                    By.CLASS_NAME, 'JobCard_jobCardContainer__l0svv')
                if len(pre) == len(next):
                    break
                else:
                    pre = next

            find_jobs(driver, job_type)
            print(SCRAPING_ENDED)
        else:
            print(LOGIN_FAILED)
        driver.quit()
    except Exception as e:
        saveLogs(e)
        print(e)


# glassdoor('https://www.glassdoor.com/Job/remote-aws-engineer-jobs-SRCH_IL.0,6_IS11047_KO7,19.htm?fromAge=3', '')
