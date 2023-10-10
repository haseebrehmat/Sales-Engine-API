from scraper.utils.helpers import configure_webdriver

import time

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type
from utils.helpers import saveLogs
from scraper.models.accounts import Accounts

def get_job_url(job):
    return job.find_element(By.CLASS_NAME, 'job-title').get_attribute('href')


def get_job_detail(driver, job_source, job_url, job_type):
    try:
        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        job_title = driver.find_element(By.CLASS_NAME, "title").text
        company_name = driver.find_element(By.CLASS_NAME, "company-name").text
        job_description = driver.find_element(By.CLASS_NAME, "jfJgbU")

        job = {
            "job_title": job_title,
            "company_name": company_name,
            "address": "",
            "job_description": job_description.text,
            "job_source_url": job_url,
            "job_posted_date": "",
            "salary_format": "N/A",
            "estimated_salary": "N/A",
            "salary_min": "N/A",
            "salary_max": "N/A",
            "job_source": job_source,
            "job_type": set_job_type(job_type),
            "job_description_tags": job_description.get_attribute('innerHTML')
        }

        about_job_lines = driver.find_elements(By.CLASS_NAME, "value")
        try:
            job['address'] = about_job_lines[0].text
        except Exception as e:
            print(e)
        try:
            job['estimated_salary'] = k_conversion(about_job_lines[1].text)
        except Exception as e:
            print(e)
        try:
            job['job_posted_date'] = about_job_lines[4].text.split('\n')[1]
        except Exception as e:
            print(e)
        return job, False
    except Exception as e:
        saveLogs(e)
        return None, True

def find_jobs(driver, job_type):
    scrapped_data = []

    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "salary_format", "estimated_salary", "salary_min", "salary_max", "job_source", "job_type",
                    "job_description_tags"]
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "job-card")))
        time.sleep(3)

        start = 0
        for i in range(10):
            jobs = driver.find_elements(By.CLASS_NAME, "job-card")
            for job in jobs[start:]:
                job.location_once_scrolled_into_view
            start = len(jobs) - 1
            time.sleep(2)

        jobs = driver.find_elements(By.CLASS_NAME, "job-card")

        job_urls = [get_job_url(job) for job in jobs]

        count = 0
        total_jobs = len(job_urls)

        for job_url in job_urls:
            try:
                driver.get(job_url)
                job, error = get_job_detail(driver, 'arcdev', job_url, job_type)
                if not error:
                    data = [job[c] for c in columns_name]
                    scrapped_data.append(data)
                    # upload jobs by 20 records
                    count += 1

                if scrapped_data and count > 0 and (count%20 == 0 or count == total_jobs - 1):
                    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
                    filename = generate_scraper_filename(ScraperNaming.ARC_DEV)
                    df.to_excel(filename, index=False)
                    ScraperLogs.objects.create(total_jobs=len(df), job_source='Arc Dev', filename=filename)
                    scrapped_data = []
                time.sleep(2)
            except Exception as e:
                print(e)
                saveLogs(e)
    except Exception as e:
        saveLogs(e)

def login(driver, email, password):
    login_status = False
    name_input = driver.find_element(By.NAME, "email")
    name_input.clear()
    name_input.send_keys(email)
    time.sleep(3)
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, "action-login").click()
    time.sleep(3)
    try:
        driver.find_element(By.CLASS_NAME, "action-login")
    except Exception as e:
        login_status = True
    return login_status

def arc_dev(link, job_type):
    try:
        print("Start in try portion. \n")
        queryset = Accounts.objects.all()
        login_status = False
        for account in queryset:
            driver = configure_webdriver()
            driver.maximize_window()
            driver.get(link)
            login_status = login(driver, account.email, account.password)
            if login_status:
                break
            else:
                driver.quit()
        try:
            print("Fetching...")
            find_jobs(driver, job_type)
        except Exception as e:
            saveLogs(e)
            print("out from for loop")
        driver.quit()

    except Exception as e:
        saveLogs(e)
        print("Error Occurs. \n")
